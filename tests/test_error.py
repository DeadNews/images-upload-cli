import pytest
from httpx import HTTPError, Response, codes, post
from images_upload_cli.error import raise_on_error
from pytest_httpx import HTTPXMock


def test_raise_on_error_success():
    response = Response(status_code=codes.OK)
    raise_on_error(response)


def test_raise_on_error_client_error(httpx_mock: HTTPXMock):
    # Mock the response.
    httpx_mock.add_response(status_code=codes.NOT_FOUND)
    response = post(url="https://example.com")

    with pytest.raises(HTTPError) as exc_info:
        raise_on_error(response)

    assert (
        str(exc_info.value)
        == "Client error '404 Not Found' for url 'https://example.com'. Response text below:\n\n"
    )


def test_raise_on_error_invalid_status_code(httpx_mock: HTTPXMock):
    # Mock the response.
    httpx_mock.add_response(status_code=999)
    response = post(url="https://example.com")

    with pytest.raises(HTTPError) as exc_info:
        raise_on_error(response)

    assert (
        str(exc_info.value)
        == "Invalid status code '999 ' for url 'https://example.com'. Response text below:\n\n"
    )
