import logging

from images_upload_cli.logger import ErrorHandler, setup_logger


def test_errorhandler_emit():
    handler = ErrorHandler()
    record = logging.LogRecord(
        "test", logging.ERROR, "test_logger.py", 10, "Error message", None, None
    )
    handler.emit(record)
    assert handler.has_error_occurred() is True


def test_errorhandler_emit_no_error():
    handler = ErrorHandler()
    record = logging.LogRecord(
        "test", logging.INFO, "test_logger.py", 10, "Info message", None, None
    )
    handler.emit(record)
    assert handler.has_error_occurred() is False


def test_setup_logger():
    log_level = "DEBUG"
    error_handler = setup_logger(log_level)

    # Add your assertions here to verify the logging behavior
    assert isinstance(error_handler, ErrorHandler)
