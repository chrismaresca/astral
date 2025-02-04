# -------------------------------------------------------------------------------- #
# Message Template Validation
# -------------------------------------------------------------------------------- #

# Built-in imports
from typing import Any, Dict, Literal, Optional, Type, Set, get_origin, get_args, Sequence
import string
# Pydantic imports
from pydantic import BaseModel

# Jinja2 imports
from jinja2 import BaseLoader, meta

# Internal (project-specific) imports
from astral_ai.logger import logger
from astral_ai.messages.exceptions import (
    PythonTemplateKeyError,
    StringTemplateError,
    Jinja2TemplateParsingError,
    Jinja2TemplateRenderError,
)

from astral_ai.messages.template_manager import TemplateManager


# -------------------------------------------------------------------------------- #
# Helper Functions
# -------------------------------------------------------------------------------- #


# -------------------------------------------------------------------------------- #
# Find String Placeholders
# -------------------------------------------------------------------------------- #


def find_string_placeholders(text: str) -> Set[str]:
    """
    Given a Python-format-compatible string, return a set of placeholder field names.

    Example:
        text = "Hello, {name}! Today is {day}."
        placeholders = _find_string_placeholders(text)
        # placeholders -> {"name", "day"}
    """
    formatter = string.Formatter()
    placeholders = set()
    for _, field_name, _, _ in formatter.parse(text):
        if field_name is not None:
            placeholders.add(field_name)
    return placeholders


# -------------------------------------------------------------------------------- #
# Validate Type
# -------------------------------------------------------------------------------- #


def validate_type(var_name: str, expected_type: Type, value: Any) -> None:
    """
    Validates that 'value' matches the 'expected_type'.

    For container types (e.g. List[Item]), each element is validated.
    For Pydantic BaseModel subclasses, if value is a dict, an attempt is made to parse it.

    Raises:
        TypeError: if the type of value does not match expected_type.
    """
    origin = get_origin(expected_type)
    if origin is not None:
        # Validate container type (e.g., List[Item])
        if not isinstance(value, origin):
            raise TypeError(
                f"Variable '{var_name}' is expected to be of type {origin.__name__}, "
                f"but got type {type(value).__name__}."
            )
        inner_types = get_args(expected_type)
        if inner_types:
            inner_type = inner_types[0]
            if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
                for i, item in enumerate(value):
                    validate_type(f"{var_name}[{i}]", inner_type, item)
    else:
        # For Pydantic models, allow dict parsing.
        if isinstance(expected_type, type) and issubclass(expected_type, BaseModel):
            if isinstance(value, dict):
                try:
                    expected_type.parse_obj(value)
                except Exception as e:
                    raise TypeError(
                        f"Variable '{var_name}' expected type {expected_type.__name__}, "
                        f"but could not parse dict: {e}"
                    ) from e
            elif not isinstance(value, expected_type):
                raise TypeError(
                    f"Variable '{var_name}' is expected to be of type {expected_type.__name__}, "
                    f"but got type {type(value).__name__}."
                )
        else:
            # Standard type check.
            if not isinstance(value, expected_type):
                raise TypeError(
                    f"Variable '{var_name}' is expected to be of type {expected_type.__name__}, "
                    f"but got type {type(value).__name__}."
                )


# -------------------------------------------------------------------------------- #
# Detect Template Variables
# -------------------------------------------------------------------------------- #


def detect_template_variables(
    template_source: str,
    engine: Literal["python", "jinja2"],
    template_path: Optional[str] = None,
    loader: Optional[BaseLoader] = None
) -> Set[str]:
    """
    Detects placeholders in the template.

    For the Python engine, uses a simple string placeholder detector.
    For Jinja2, leverages Jinja2's meta API.
    """
    if engine == "python":
        return find_string_placeholders(template_source)
    elif engine == "jinja2":
        try:
            tm = TemplateManager.get_instance(template_path=template_path, loader=loader)
            source_str, _, _ = tm.environment.loader.get_source(tm.environment, template_source)
            parsed_content = tm.environment.parse(source_str)
            return meta.find_undeclared_variables(parsed_content)
        except Exception as e:
            logger.error("Error detecting variables in Jinja2 template.")
            raise Jinja2TemplateParsingError(
                f"Error parsing Jinja2 template '{template_source}': {e}"
            ) from e
    else:
        raise ValueError(f"Unsupported template engine: {engine}")


# -------------------------------------------------------------------------------- #
# Perform Type Checking
# -------------------------------------------------------------------------------- #


def perform_type_checking(required_vars_and_types: Dict[str, Type], template_args: Dict[str, Any]) -> None:
    """
    Validates that the values in template_args match the expected types defined in required_vars_and_types.
    """
    for var, expected_type in required_vars_and_types.items():
        if var in template_args and expected_type is not Any:
            try:
                validate_type(var, expected_type, template_args[var])
            except TypeError as e:
                logger.error(str(e))
                raise


# -------------------------------------------------------------------------------- #
# Render Template Content
# -------------------------------------------------------------------------------- #


def render_template_content(
    template_source: str,
    engine: Literal["python", "jinja2"],
    template_args: Dict[str, Any],
    template_path: Optional[str] = None,
    loader: Optional[BaseLoader] = None
) -> str:
    """
    Renders the template using the specified engine.
    """
    if engine == "python":
        try:
            return template_source.format(**template_args)
        except KeyError as e:
            logger.error("Missing key during Python template rendering.")
            raise PythonTemplateKeyError(f"Missing key in Python template: {e}") from e
        except ValueError as e:
            logger.error("Error in Python template formatting.")
            raise StringTemplateError(f"Malformed Python template: {e}") from e
    elif engine == "jinja2":
        try:
            tm = TemplateManager.get_instance(template_path=template_path, loader=loader)
            jinja_template = tm.get_template(template_source)
            return jinja_template.render(**template_args)
        except Exception as e:
            logger.error("Error rendering Jinja2 template.")
            raise Jinja2TemplateRenderError(
                f"Failed to render Jinja2 template '{template_source}': {e}"
            ) from e
    else:
        raise ValueError(f"Unsupported template engine: {engine}")
