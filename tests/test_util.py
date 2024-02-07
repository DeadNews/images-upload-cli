from io import BytesIO
from os import environ
from platform import system

import pytest
from images_upload_cli.util import (
    GetEnvError,
    get_env,
    get_font,
    get_img_ext,
    human_size,
    make_thumbnail,
    search_font,
)
from PIL import Image, ImageFont


@pytest.mark.parametrize(
    ("test_arg", "expected"),
    [
        (1, "1.0 B"),
        (300, "300.0 B"),
        (3000, "2.9 KiB"),
        (3000000, "2.9 MiB"),
        (1024, "1.0 KiB"),
        (10**26 * 30, "2481.5 YiB"),
    ],
)
def test_human_size(test_arg: int, expected: str) -> None:
    """
    Test the human_size function.

    Args:
        test_arg (int): The number of bytes to be converted.
        expected (str): The expected human-readable size with the appropriate unit and suffix.

    Raises:
        AssertionError: If the output of calling human_size with (negation of) test_arg is not equal to (negation of) expected.
    """
    assert human_size(test_arg) == expected

    args_with_negative = -test_arg
    assert human_size(args_with_negative) == f"-{expected}"


def test_make_thumbnail():
    # Create a sample image
    image = Image.new("RGBA", (500, 500))
    image_bytes = BytesIO()
    image.save(image_bytes, format="PNG")
    image_bytes.seek(0)

    # Create a sample font
    font = ImageFont.load_default(size=12)

    # Call the make_thumbnail function
    thumbnail = make_thumbnail(image_bytes.read(), font, size=(300, 300))

    # Check if the thumbnail has the desired size and format
    thumbnail_image = Image.open(BytesIO(thumbnail))
    assert thumbnail_image.size == (300, 300 + 16)
    assert thumbnail_image.format == "JPEG"


def test_get_img_ext(img: bytes) -> None:
    assert get_img_ext(img) == "png"


def test_get_font() -> None:
    assert isinstance(get_font(), ImageFont.FreeTypeFont)


def test_search_font_error():
    fonts = ["Font1", "Font2"]
    with pytest.raises(GetEnvError):
        search_font(fonts)


def test_get_font_env() -> None:
    if system() == "Linux":
        environ["CAPTION_FONT"] = "DejaVuSerif"
    elif system() == "Darwin":
        environ["CAPTION_FONT"] = "Helvetica"
    elif system() == "Windows":
        environ["CAPTION_FONT"] = "arial"

    assert isinstance(get_font(), ImageFont.FreeTypeFont)


def test_get_env() -> None:
    environ["TEST_KEY_1"] = "test"
    assert get_env("TEST_KEY_1") == "test"


def test_get_env_error() -> None:
    with pytest.raises(GetEnvError):
        get_env("TEST_KEY_2")
