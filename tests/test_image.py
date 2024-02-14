from io import BytesIO
from os import environ
from platform import system

import pytest
from images_upload_cli.image import get_font, get_img_ext, make_thumbnail, search_font
from images_upload_cli.util import GetEnvError
from PIL import Image, ImageFont


def test_make_thumbnail():
    # Create a sample image
    image = Image.new("RGBA", (600, 600))
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
