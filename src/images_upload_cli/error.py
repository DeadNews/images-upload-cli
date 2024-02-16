"""Error handling and exception classes."""

from httpx import Response
from loguru import logger


class GetEnvError(Exception):
    """Exception raised when an environment variable is not found."""


def log_on_error(response: Response) -> None:
    """
    Logs an error message based on the HTTP response.

    Args:
        response (Response): The HTTP response object.

    Returns:
        None
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
    logger.debug(f"Response text:\n\n{response.text}")
