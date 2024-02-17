from pathlib import Path

import pytest
from dotenv import load_dotenv
from httpx import AsyncClient
from images_upload_cli.cli import upload_images
from images_upload_cli.upload import UPLOAD
from pytest_httpx import HTTPXMock

from tests.mock import MOCK_HOSTINGS, RESPONSE


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    ("hosting", "mock_text", "mock_link"),
    [
        pytest.param(hosting, RESPONSE[hosting][0], RESPONSE[hosting][1], id=hosting)
        for hosting in MOCK_HOSTINGS
    ],
)
async def test_upload_funcs(
    httpx_mock: HTTPXMock,
    hosting: str,
    mock_text: str,
    mock_link: str,
    img: bytes,
) -> None:
    """
    Test the image upload functionality of different hosting services.

    Args:
        httpx_mock (HTTPXMock): An instance of the HTTPXMock class used for mocking HTTP responses.
        hosting (str): A string representing the hosting service to test.
        mock_text (str): A string representing the mock response text.
        mock_link (str): A string representing the expected link after image upload.
        img (bytes): Bytes of the image to be uploaded.

    Raises:
        AssertionError: If the returned link is not equal to the expected mock_link.
    """
    # Mock the response
    httpx_mock.add_response(text=mock_text)

    # Load environment variables
    load_dotenv(dotenv_path="tests/data/.env.sample")

    # Upload the image
    async with AsyncClient() as client:
        upload_func = UPLOAD[hosting]
        link = await upload_func(client, img)
        assert link == mock_link


@pytest.mark.asyncio()
@pytest.mark.parametrize("hosting", MOCK_HOSTINGS)
async def test_upload_funcs_error(
    httpx_mock: HTTPXMock,
    hosting: str,
    img: bytes,
) -> None:
    """
    Test the image upload functionality of different hosting services when an error occurs.

    Args:
        httpx_mock (HTTPXMock): An instance of the HTTPXMock class used for mocking HTTP responses.
        hosting (str): A string representing the hosting service to test.
        img (bytes): Bytes of the image to be uploaded.

    Raises:
        AssertionError: If the returned result is not empty.
    """
    # Mock the response
    httpx_mock.add_response(json={"error": "Upload failed"}, status_code=500)

    # Load environment variables
    load_dotenv(dotenv_path="tests/data/.env.sample")

    # Upload the image
    async with AsyncClient() as client:
        upload_func = UPLOAD[hosting]
        result = await upload_func(client, img)

    # Assert the result is empty
    assert result == ""


@pytest.mark.asyncio()
@pytest.mark.parametrize("hosting", ["fastpic", "imagebin"])
async def test_upload_funcs_not_found(
    httpx_mock: HTTPXMock,
    hosting: str,
    img: bytes,
) -> None:
    """
    Test the error handling of image upload functionality for specific hosting services.

    Args:
        httpx_mock (HTTPXMock): An instance of the HTTPXMock class used for mocking HTTP responses.
        hosting (str): A string representing the hosting service to test.
        img (bytes): Bytes of the image to be uploaded.

    Raises:
        AssertionError: If the result is not empty.
    """
    # Mock the response
    httpx_mock.add_response(text="Response without the url.")

    # Upload the image
    async with AsyncClient() as client:
        upload_func = UPLOAD[hosting]
        result = await upload_func(client, img)

    # Assert the result is empty
    assert result == ""


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
        bbcode=False,
        thumbnail=thumbnail,
    )

    if thumbnail:
        assert result == [f"[url={mock_link}][img]{mock_link}[/img][/url]"]
    else:
        assert result == [mock_link]
