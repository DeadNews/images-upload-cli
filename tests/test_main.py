from pathlib import Path

import pytest
from pytest_httpx import HTTPXMock

from images_upload_cli.main import format_link, upload_images
from images_upload_cli.upload import UPLOAD
from tests.mock import RESPONSE


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "thumbnail",
    [pytest.param(False, id="default"), pytest.param(True, id="thumbnail")],
)
async def test_upload_images_coroutine(httpx_mock: HTTPXMock, thumbnail: bool) -> None:
    """Test the upload_images coroutine.

    Args:
        httpx_mock: An instance of the HTTPXMock class used for mocking HTTP responses.
        thumbnail: A boolean flag indicating whether to generate thumbnail images for the uploaded images.

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


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "thumbnail",
    [pytest.param(False, id="default"), pytest.param(True, id="thumbnail")],
)
async def test_upload_images_upload_failure(httpx_mock: HTTPXMock, thumbnail: bool) -> None:
    """Test the upload_images coroutine when the upload fails for an image.

    Args:
        httpx_mock: An instance of the HTTPXMock class used for mocking HTTP responses.
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


def test_format_link_plain():
    links = [("https://example.com/image1.jpg", None), ("https://example.com/image2.jpg", None)]
    fmt = "plain"
    expected_output = "https://example.com/image1.jpg https://example.com/image2.jpg"
    assert format_link(links, fmt) == expected_output


def test_format_link_bbcode():
    links = [
        ("https://example.com/image1.jpg", "https://example.com/thumb1.jpg"),
        ("https://example.com/image2.jpg", None),
    ]
    fmt = "bbcode"
    expected_output = "[url=https://example.com/image1.jpg][img]https://example.com/thumb1.jpg[/img][/url] [img]https://example.com/image2.jpg[/img]"

    assert format_link(links, fmt) == expected_output


def test_format_link_html():
    links = [
        ("https://example.com/image1.jpg", None),
        ("https://example.com/image2.jpg", "https://example.com/thumb1.jpg"),
    ]
    fmt = "html"
    expected_output = '<img src="https://example.com/image1.jpg" alt="image"> <a href="https://example.com/image2.jpg"><img src="https://example.com/thumb1.jpg" alt="thumb"></a>'
    assert format_link(links, fmt) == expected_output


def test_format_link_markdown():
    links = [
        ("https://example.com/image1.jpg", None),
        ("https://example.com/image2.jpg", "https://example.com/thumb1.jpg"),
    ]
    fmt = "markdown"
    expected_output = "![image](https://example.com/image1.jpg) [![thumb](https://example.com/thumb1.jpg)](https://example.com/image2.jpg)"
    assert format_link(links, fmt) == expected_output


def test_format_link_invalid_format():
    links = [("https://example.com/image1.jpg", None), ("https://example.com/image2.jpg", None)]
    fmt = "invalid_format"
    expected_output = ""
    assert format_link(links, fmt) == expected_output
