from pathlib import Path

import pytest
from images_upload_cli.main import upload_images
from images_upload_cli.upload import UPLOAD
from pytest_httpx import HTTPXMock

from tests.mock import RESPONSE


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "thumbnail",
    [pytest.param(False, id="default"), pytest.param(True, id="thumbnail")],
)
async def test_upload_images_coroutine(httpx_mock: HTTPXMock, thumbnail: bool) -> None:
    """
    Test the upload_images coroutine.

    Args:
        httpx_mock (HTTPXMock): An instance of the HTTPXMock class used for mocking HTTP responses.
        thumbnail (bool): A boolean flag indicating whether to generate thumbnail images for the uploaded images.

    Raises:
        AssertionError: If the returned link is not equal to the expected mock_link.
    """
    images = (Path("tests/data/pic.png"),)
    hosting = "imgur"
    mock_text = RESPONSE[hosting][0]
    mock_link = RESPONSE[hosting][1]

    # Mock the response
    httpx_mock.add_response(text=mock_text)

    # Upload the image
    result = await upload_images(
        upload_func=UPLOAD[hosting],
        images=images,
        thumbnail=thumbnail,
    )

    if thumbnail:
        assert result == [(mock_link, mock_link)]
    else:
        assert result == [(mock_link, None)]


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "thumbnail",
    [pytest.param(False, id="default"), pytest.param(True, id="thumbnail")],
)
async def test_upload_images_upload_failure(httpx_mock: HTTPXMock, thumbnail: bool) -> None:
    """
    Test the upload_images coroutine when the upload fails for an image.

    Args:
        httpx_mock (HTTPXMock): An instance of the HTTPXMock class used for mocking HTTP responses.
    """
    images = (Path("tests/data/pic.png"),)
    hosting = "imgur"

    # Mock the response
    httpx_mock.add_response(text="Upload failed.", status_code=500)

    # Upload the image
    result = await upload_images(
        upload_func=UPLOAD[hosting],
        images=images,
        thumbnail=thumbnail,
    )

    assert result == []
