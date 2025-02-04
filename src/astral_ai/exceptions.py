
# -------------------------------------------------------------------------------- #
# Exceptions
# -------------------------------------------------------------------------------- #

# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #

# Built-in
from typing import List

# Project
from astral_ai.typing.models import ModelName

# -------------------------------------------------------------------------------- #
# LLM Response Exceptions
# -------------------------------------------------------------------------------- #



# -------------------------------------------------------------------------------- #
# API Exceptions
# -------------------------------------------------------------------------------- #


class APIKeyNotFoundError(Exception):
    """
    Exception raised when an API key is not found in the environment variables.
    """

    def __init__(self, message: str = "API key not found."):
        self.message = message
        super().__init__(self.message)


# -------------------------------------------------------------------------------- #
# Messages Exceptions
# -------------------------------------------------------------------------------- #


class MissingTemplateVariablesError(Exception):
    """
    Raised when certain required template variables are missing in strict mode.

    Example:
        raise MissingTemplateVariablesError("Missing placeholders: ['name']")
    """

    def __init__(self, message: str = "Required variables are not provided to a template or string formatter when strict validation is enabled."):
        self.message = message
        super().__init__(self.message)


class PythonTemplateKeyError(Exception):
    """
    Raised when a KeyError occurs during Python string formatting,
    implying a missing placeholder variable was encountered.
    """

    def __init__(self, message: str = "A KeyError occurred while formatting a Python string template."):
        self.message = message
        super().__init__(self.message)


class StringTemplateError(Exception):
    """
    Raised for general Python string template errors,
    such as invalid format strings or other formatting issues.
    """

    def __init__(self, message: str = "An error occurred while formatting a Python string template."):
        self.message = message
        super().__init__(self.message)


class Jinja2EnvironmentError(Exception):
    """
    Raised for issues related to creating, loading, or parsing
    a Jinja2 environment (e.g., invalid directory, corrupted template, etc.).
    """

    def __init__(self, message: str = "An error occurred while creating, loading, or parsing the Jinja2 environment."):
        self.message = message
        super().__init__(self.message)


class Jinja2TemplateNotFoundError(Exception):
    """
    Raised when a specified Jinja2 template cannot be found by the environment loader.
    """
    pass


class Jinja2TemplateParsingError(Exception):
    """
    Raised when the template source cannot be parsed correctly
    (e.g., syntax error or partial corruption).
    """
    pass


class Jinja2TemplateRenderError(Exception):
    """
    Raised when rendering a Jinja2 template fails due to logic errors,
    undefined variables, or runtime exceptions in template logic.
    """
    pass
