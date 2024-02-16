from httpx import codes, post
from images_upload_cli.error import log_on_error
from pytest_httpx import HTTPXMock


def test_log_on_error(httpx_mock: HTTPXMock):
    httpx_mock.add_response(status_code=codes.NOT_FOUND, text="Page not found")
    response = post(url="https://example.com")

    log_on_error(response)
    # Add your assertions here to verify the logging behavior
