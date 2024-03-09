"""Logger configuration."""

import logging

from loguru import logger
from rich.logging import RichHandler


class ErrorHandler(logging.StreamHandler):
    """Custom error handler for logging."""

    def __init__(self: "ErrorHandler") -> None:
        """Init."""
        super().__init__()
        self.error_occurred = False

    def emit(self: "ErrorHandler", record: logging.LogRecord) -> None:
        """Emit a record."""
        if record.levelno >= logging.ERROR:
            self.error_occurred = True

    def has_error_occurred(self: "ErrorHandler") -> bool:
        """Check if an error has occurred."""
        return self.error_occurred


def setup_logger(log_level: str) -> ErrorHandler:
    """Configure logger.

    Args:
        log_level: The log level to set for the logger.

    Returns:
        ErrorHandler: The error handler associated with the logger.
    """
    logger.remove()
    # Console handler
    logger.add(
        sink=RichHandler(log_time_format="[%X]", rich_tracebacks=True),
        level=log_level,
        format=lambda _: "{message}",
    )
    # Error handler
    error_handler = ErrorHandler()
    logger.add(sink=error_handler, level="ERROR")

    return error_handler
