# -------------------------------------------------------------------------------- #
# Messages Exceptions
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


class Jinja2TemplateLoadingError(Exception):
    """
    Raised when a specified Jinja2 template cannot be found by the environment loader.
    """

    def __init__(self, message: str = "A specified Jinja2 template cannot be found by the environment loader."):
        self.message = message
        super().__init__(self.message)


class Jinja2TemplateParsingError(Exception):
    """
    Raised when the template source cannot be parsed correctly
    (e.g., syntax error or partial corruption).
    """

    def __init__(self, message: str = "The template source cannot be parsed correctly (e.g., syntax error or partial corruption)."):
        self.message = message
        super().__init__(self.message)


class Jinja2TemplateRenderError(Exception):
    """
    Raised when rendering a Jinja2 template fails due to logic errors,
    undefined variables, or runtime exceptions in template logic.
    """

    def __init__(self, message: str = "Rendering a Jinja2 template fails due to logic errors, undefined variables, or runtime exceptions in template logic."):
        self.message = message
        super().__init__(self.message)


class RequiredTemplateVariablesNotDetectedError(Exception):
    """
    Raised when required variables are provided but not found in the template.
    """
    def __init__(self, message: str = "Required variables are provided but not found in the template."):
        self.message = message
        super().__init__(self.message)
