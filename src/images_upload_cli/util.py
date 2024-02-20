"""Utility functions for the package."""

from os import getenv
from pathlib import Path
from shutil import which
from subprocess import Popen

import click
from httpx import Response
from loguru import logger


class GetEnvError(Exception):
    """Exception raised when an environment variable is not found."""


def get_config_path() -> Path:
    """Get the path to the app config file.

    Returns:
       The path to the app config file.
    """
    app_dir = click.get_app_dir("images-upload-cli")
    return Path(app_dir) / ".env"


def get_env(variable: str) -> str:
    """Get the value of an environment variable.

    Args:
        variable: The name of the environment variable to retrieve.

    Returns:
        The value of the environment variable, if found.

    Raises:
        GetEnvError: If the environment variable is not found.
    """
    if value := getenv(variable):
        return value

    msg = f"Please setup {variable} in environment variables or in '{get_config_path()}'."
    raise GetEnvError(msg)


def human_size(num: float, suffix: str = "B") -> str:
    """Convert bytes to human-readable format.

    Args:
        num: The number of bytes to be converted.
        suffix: The suffix to be appended to the converted size. Defaults to "B".

    Returns:
        The human-readable size with the appropriate unit and suffix.
    """
    units = ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]
    round_num = 1024.0

    for unit in units:
        if abs(num) < round_num:
            return f"{num:3.1f} {unit}{suffix}"
        num /= round_num

    return f"{num:.1f} Yi{suffix}"


def notify_send(text_to_print: str) -> None:
    """Send desktop notifications via libnotify.

    Args:
        text_to_print: The text to be displayed in the desktop notification.
    """
    if notify_send := which("notify-send"):
        Popen([notify_send, "-a", "images-upload-cli", text_to_print])  # noqa: S603


def log_on_error(response: Response) -> None:
    """Logs an error message based on the HTTP response.

    Args:
        response: The HTTP response object.
    """
    status_class = response.status_code // 100
    error_types = {
        1: "Informational response",
        3: "Redirect response",
        4: "Client error",
        5: "Server error",
    }
    error_type = error_types.get(status_class, "Invalid status code")

    logger.error(
        f"{error_type} '{response.status_code} {response.reason_phrase}' for url '{response.url}'."
    )
    logger.debug(f"Response text:\n{response.text}")
