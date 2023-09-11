#!/usr/bin/env python
import pytest
from dotenv import load_dotenv
from httpx import AsyncClient
from images_upload_cli.upload import UPLOAD
from pytest_httpx import HTTPXMock

from tests.mock import HOSTINGS, RESPONSE


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    ("hosting", "mock_text", "mock_link"),
    [
        pytest.param(hosting, RESPONSE[hosting][0], RESPONSE[hosting][1], id=hosting)
        for hosting in HOSTINGS
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
    # Mock the response.
    httpx_mock.add_response(text=mock_text)

    # Load environment variables.
    load_dotenv(dotenv_path="tests/data/.env.sample")

    # Upload the image.
    async with AsyncClient() as client:
        upload_func = UPLOAD[hosting]
        link = await upload_func(client, img)
        assert link == mock_link
