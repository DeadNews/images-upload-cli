from httpx import codes, post
from images_upload_cli.error import log_on_error
from logot import Logot, logged
from pytest_httpx import HTTPXMock


def test_log_on_error(httpx_mock: HTTPXMock, logot: Logot):
    """
    Test the log_on_error function when a client error occurs.

    Args:
        httpx_mock (HTTPXMock): The HTTPXMock object for mocking HTTP requests.
        logot (Logot): The Logot object for logging.
    """
    # Mock the response
    httpx_mock.add_response(status_code=codes.NOT_FOUND, text="Page not found")

    response = post(url="https://example.com")
    log_on_error(response)

    # Assert the log messages
    logot.assert_logged(
        logged.error("Client error '404 Not Found' for url 'https://example.com'.")
    )
    logot.assert_logged(logged.debug("Response text:\nPage not found"))
