# -------------------------------------------------------------------------------- #
# Message Template
# -------------------------------------------------------------------------------- #

"""
This module provides a class for creating text messages from templates.

The MessageTemplate class allows you to:    

1. Create a MessageTemplate instance from a plain string template or a Jinja2 template.
2. Render the template with provided arguments to create a TextMessage instance.
3. Convenience method to create and render a TextMessage in one call.


"""

# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #

# Built-in imports
from pydantic import BaseModel, Field
from typing import Any, Dict, Literal, Optional, Type
from collections.abc import Sequence

# Third-party imports
from jinja2 import BaseLoader

# Logger
from astral_ai.logger import logger

# Exceptions
from astral_ai.messages.exceptions import (
    MissingTemplateVariablesError,
    RequiredTemplateVariablesNotDetectedError,
)

# Template Validation
from astral_ai.messages.utils import (
    detect_template_variables,
    perform_type_checking,
    render_template_content,
)

# Message Models
from astral_ai.typing.messages import (
    MessageRole,
    TextMessage,
)

# -------------------------------------------------------------------------------- #
# MessageTemplate Class (TextMessage Only)
# -------------------------------------------------------------------------------- #


class MessageTemplate:
    """
    A blueprint for creating text messages via template rendering.

    This class is initialized with a template (either a filename or a text string)
    and configuration about how to render it. It auto-detects required placeholders (if not provided)
    and performs type-checking when rendering.
    """

    def __init__(
        self,
        template_source: str,
        engine: Literal["python", "jinja2"] = "python",
        role: MessageRole = "user",
        required_vars_and_types: Optional[Dict[str, Type]] = None,
        template_path: str = "src/templates",
        loader: Optional[BaseLoader] = None,
    ):
        self.template_source = template_source
        self.engine = engine
        self.role = role
        self.template_path = template_path
        self.loader = loader

        # Auto-detect placeholders if type-checking specs are not provided.
        detected_vars = detect_template_variables(
            template_source, engine, template_path, loader
        )
        if required_vars_and_types is None:
            logger.warning(
                "Type checking is disabled because no required_vars_and_types were provided. "
                "Be cautious in production."
            )
            self.required_vars_and_types = {var: Any for var in detected_vars}
        else:
            missing_in_template = set(required_vars_and_types.keys()) - detected_vars
            if missing_in_template:
                logger.error(
                    "The following required variables were provided but not found in the template: %s",
                    missing_in_template
                )
                raise RequiredTemplateVariablesNotDetectedError(
                    f"The following required variables were provided but not found in the template: {missing_in_template}"
                )
            self.required_vars_and_types = {
                k: v for k, v in required_vars_and_types.items() if k in detected_vars
            }

    @classmethod
    def from_string_template(
        cls,
        template_source: str,
        role: MessageRole = "user",
        required_vars_and_types: Optional[Dict[str, Type]] = None,
        template_path: str = "src/templates",
        loader: Optional[BaseLoader] = None,
    ) -> "MessageTemplate":
        """
        Factory method to create a MessageTemplate instance using a plain string template.
        """
        return cls(
            template_source=template_source,
            engine="python",
            role=role,
            required_vars_and_types=required_vars_and_types,
            template_path=template_path,
            loader=loader,
        )

    @classmethod
    def from_jinja_template(
        cls,
        template_source: str,
        role: MessageRole = "user",
        required_vars_and_types: Optional[Dict[str, Type]] = None,
        template_path: str = "src/templates",
        loader: Optional[BaseLoader] = None,
    ) -> "MessageTemplate":
        """
        Factory method to create a MessageTemplate instance using a Jinja2 template.
        """
        return cls(
            template_source=template_source,
            engine="jinja2",
            role=role,
            required_vars_and_types=required_vars_and_types,
            template_path=template_path,
            loader=loader,
        )

    def to_message(
        self,
        template_args: Optional[Dict[str, Any]] = None,
        require_all: bool = True
    ) -> TextMessage:
        """
        Renders the template with the provided arguments and returns a TextMessage instance.
        """
        template_args = template_args or {}

        if require_all:
            missing = set(self.required_vars_and_types.keys()) - set(template_args.keys())
            if missing:
                msg = f"Missing required template variables: {missing}"
                logger.error(msg)
                raise MissingTemplateVariablesError(msg)

        perform_type_checking(self.required_vars_and_types, template_args)

        rendered_text = render_template_content(
            self.template_source,
            self.engine,
            template_args,
            self.template_path,
            self.loader
        )

        return TextMessage(role=self.role, text=rendered_text)

    @classmethod
    def create_message(
        cls,
        template_source: str,
        template_args: Optional[Dict[str, Any]] = None,
        engine: Literal["python", "jinja2"] = "python",
        role: MessageRole = "user",
        required_vars_and_types: Optional[Dict[str, Type]] = None,
        template_path: str = "src/templates",
        loader: Optional[BaseLoader] = None,
        require_all: bool = True
    ) -> TextMessage:
        """
        Convenience method to create and render a TextMessage in one call.
        """
        instance = cls(
            template_source=template_source,
            engine=engine,
            role=role,
            required_vars_and_types=required_vars_and_types,
            template_path=template_path,
            loader=loader,
        )
        return instance.to_message(template_args=template_args, require_all=require_all)
