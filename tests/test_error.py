import pytest
from httpx import HTTPError, Response, codes, post
from images_upload_cli.error import raise_on_error
from pytest_httpx import HTTPXMock


def test_raise_on_error_success():
    response = Response(status_code=codes.OK)
    raise_on_error(response)


def test_raise_on_error_error(httpx_mock: HTTPXMock):
    # Mock the response.
    httpx_mock.add_response(status_code=codes.BAD_REQUEST)
    response = post(url="https://nonexistent.test")

    with pytest.raises(HTTPError):
        raise_on_error(response)
