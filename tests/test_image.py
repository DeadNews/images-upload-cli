from io import BytesIO

import pytest
from PIL import Image, ImageFont
from pytest_mock import MockerFixture

from images_upload_cli.image import get_font, get_img_ext, make_thumbnail, search_font
from images_upload_cli.util import GetEnvError


@pytest.fixture
def font_name() -> str:
    return "tests/data/DejaVuSerif.ttf"


def test_make_thumbnail(font_name: str):
    # Create a sample image
    image = Image.new("RGBA", (600, 600))
    image_bytes = BytesIO()
    image.save(image_bytes, format="PNG")
    image_bytes.seek(0)

    # Create a sample font
    font = ImageFont.truetype(font_name, size=12)

    # Call the make_thumbnail function
    thumbnail = make_thumbnail(image_bytes.read(), font, size=(300, 300))

    # Check if the thumbnail has the desired size and format
    thumbnail_image = Image.open(BytesIO(thumbnail))
    assert thumbnail_image.size == (300, 300 + 16)
    assert thumbnail_image.format == "JPEG"


def test_get_img_ext(img: bytes) -> None:
    assert get_img_ext(img) == "png"


def test_get_font() -> None:
    font = get_font()
    assert isinstance(font, ImageFont.FreeTypeFont)


def test_get_font_custom_size() -> None:
    size = 16
    font = get_font(size=size)
    assert isinstance(font, ImageFont.FreeTypeFont)
    assert font.size == size


def test_get_font_from_env(mocker: MockerFixture, font_name: str) -> None:
    variable = "CAPTION_FONT"
    value = font_name
    mocker.patch.dict("os.environ", {variable: value})
    font = get_font()
    assert isinstance(font, ImageFont.FreeTypeFont)
    assert font.path == font_name


def test_search_font(font_name: str):
    fonts = [font_name]
    font = search_font(fonts)
    assert isinstance(font, ImageFont.FreeTypeFont)
    assert font.path == font_name


def test_search_font_not_found():
    fonts = ["NonExistentFont1", "NonExistentFont2"]
    with pytest.raises(GetEnvError):
        search_font(fonts)
