# -------------------------------------------------------------------------------- #
# Template Manager
# -------------------------------------------------------------------------------- #

# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #

# built-in imports
import os
from typing import Optional

# third-party imports
from jinja2 import Environment, FileSystemLoader, BaseLoader

# Logger
from astral_ai.logger import logger

# Exceptions
from astral_ai.messages.exceptions import (
    Jinja2EnvironmentError,
    Jinja2TemplateLoadingError,

)


# -------------------------------------------------------------------------------- #


class TemplateManager:
    """
    Singleton class to create and manage a Jinja2 environment.
    Supports any Jinja2 loader (e.g. remote loaders) by allowing a custom loader to be provided.
    """

    _instance: Optional["TemplateManager"] = None

    def __init__(self,
                 template_path: Optional[str] = "src/templates",
                 loader: Optional[BaseLoader] = None) -> None:
        """
        Initializes a Jinja2 Environment using either a custom loader or a FileSystemLoader.

        Args:
            template_path (Optional[str]): The file system path to load templates from.
                This is used only if no custom loader is provided.
            loader (Optional[BaseLoader]): A custom Jinja2 loader instance (e.g. remote loader).

        Raises:
            Jinja2EnvironmentError: If no loader is provided and template_path is not a valid directory.
        """
        # If a custom loader is provided, use it.
        if loader is not None:
            self.loader = loader
            if template_path:
                # Inform that template_path is provided but will be ignored in favor of the custom loader.
                logger.info(f"Custom loader provided; the template_path '{template_path}' will be ignored.")
            # For informational purposes, record the loader type.
            self.environment_path = None
        else:
            # Without a custom loader, template_path must be valid.
            if not template_path or not os.path.isdir(template_path):
                raise Jinja2EnvironmentError(f"Provided path '{template_path}' does not exist or is not a directory.")
            self.environment_path = template_path
            self.loader = FileSystemLoader(template_path)
            logger.info(f"FileSystemLoader configured for path: {template_path}")

        self.environment = Environment(loader=self.loader)
        logger.info("Jinja2 Environment created.")

    @classmethod
    def get_instance(cls,
                     template_path: Optional[str] = "src/templates",
                     loader: Optional[BaseLoader] = None) -> "TemplateManager":
        """
        Retrieve or create the singleton instance of the TemplateManager.

        Args:
            template_path (Optional[str]): Path to load templates from (used only if loader is not provided).
            loader (Optional[BaseLoader]): Custom Jinja2 loader to be used.

        Returns:
            TemplateManager: The singleton instance.

        Notes:
            If the instance already exists, and different parameters are provided,
            a warning is logged and the existing instance is reused.
        """
        if cls._instance is None:
            logger.info("Creating new TemplateManager instance.")
            cls._instance = cls(template_path=template_path, loader=loader)
        else:
            # Warn if the caller attempts to reinitialize with different parameters.
            if loader is not None:
                logger.warning(
                    "TemplateManager already initialized with a loader. "
                    "New loader parameter will be ignored."
                )
            elif template_path and cls._instance.environment_path != template_path:
                logger.warning(
                    "TemplateManager requested with a different template_path than the existing instance. "
                    f"Existing path: {cls._instance.environment_path}, new path: {template_path}. "
                    "Reusing the existing environment."
                )
        return cls._instance

    def get_template(self, template_name: str):
        """
        Retrieve a Jinja2 template object by name.

        Args:
            template_name (str): The name of the template to load.

        Returns:
            Template: A Jinja2 Template object.

        Raises:
            Jinja2EnvironmentError: If the template cannot be loaded.
        """
        try:
            template = self.environment.get_template(template_name)
            logger.debug(f"Loaded Jinja2 template: {template_name}")
            return template
        except Exception as e:
            logger.error(f"Error retrieving Jinja2 template '{template_name}': {e}")
            raise Jinja2TemplateLoadingError(f"Could not load template '{template_name}'")




