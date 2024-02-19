"""Image processing and manipulation."""

from io import BytesIO
from os import getenv

from PIL import Image, ImageDraw, ImageFont

from images_upload_cli.util import GetEnvError, get_config_path, human_size


def get_img_ext(img: bytes) -> str:
    """Get the extension of an image from a byte string.

    Args:
        img: A byte string representing an image.

    Returns:
        The extension of the image file.
    """
    with BytesIO(img) as f:
        ext = Image.open(f).format
        return "" if ext is None else ext.lower()


def get_font(size: int = 14) -> ImageFont.FreeTypeFont:
    """Get font for thumbnail captions.

    Args:
        size: The size of the font. Defaults to 14.

    Returns:
        ImageFont.FreeTypeFont: Represents the font.
    """
    if font_name := getenv("CAPTION_FONT"):
        return ImageFont.truetype(font_name, size=size)

    default_fonts = [
        "Helvetica",
        "NotoSerif-Regular",
        "Menlo",
        "DejaVuSerif",
        "arial",
    ]
    return search_font(fonts=default_fonts, size=size)


def search_font(fonts: list[str], size: int = 14) -> ImageFont.FreeTypeFont:
    """Attempt to retrieve a TTF font from the system.

    Args:
        fonts: A list of font names to search for.
        size (optional): The font size. Defaults to 14.

    Returns:
        ImageFont.FreeTypeFont: Represents the font.

    Raises:
        GetEnvError: If none of the default fonts are found.
    """
    for font_name in fonts:
        try:
            return ImageFont.truetype(font_name, size=size)
        except OSError:  # noqa: PERF203
            continue

    msg = (
        f"None of the fonts were found: {fonts}.\n"
        f"Please setup CAPTION_FONT in environment variables or in '{get_config_path()}'.",
    )
    raise GetEnvError(msg)


def make_thumbnail(
    img: bytes,
    font: ImageFont.FreeTypeFont,
    size: tuple[int, int] = (300, 300),
) -> bytes:
    """Generate thumbnail for the image.

    Args:
        img: The input image in bytes format.
        font: The font to be used for the text caption.
        size (optional): The desired size of the thumbnail image.

    Returns:
        The modified image in bytes format.
    """
    # Open the input image and create a copy in RGB format.
    im = Image.open(BytesIO(img))
    if im.mode != "RGB":
        im = im.convert("RGB")

    # Resize the image to the desired size using Lanczos resampling.
    pw = im.copy()
    pw.thumbnail(size=size, resample=Image.LANCZOS)

    # Create a blank image for the text
    pw_with_line = Image.new(
        mode="RGB",
        size=(pw.width, pw.height + 16),
        color=(255, 255, 255),
    )
    pw_with_line.paste(pw, box=(0, 0))

    # Get the file size of the input image.
    fsize = human_size(len(img))

    # Draw the text caption
    d = ImageDraw.Draw(pw_with_line)
    d.text(
        xy=(pw.width / 5, pw.height),
        text=f"{im.width}x{im.height} ({im.format}) [{fsize}]",
        font=font,
        fill=(0, 0, 0),
    )

    # Save the modified image as a JPEG file in bytes format.
    buffer = BytesIO()
    pw_with_line.save(
        buffer,
        format="JPEG",
        quality=95,
        optimize=True,
        progressive=True,
    )

    return buffer.getvalue()
