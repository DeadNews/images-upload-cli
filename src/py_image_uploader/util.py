#!/usr/bin/env python
from io import BytesIO
from os import getenv
from pathlib import Path
from shutil import which
from subprocess import Popen

from PIL import Image, ImageDraw, ImageFont


def get_env_val(key: str) -> str:
    value = getenv(key)
    if value is None:
        raise Exception(f"Please setup the .env variable {key}.")
    return value


def human_size(size: float) -> str:
    """
    This function will convert bytes to MB... GB... etc
    """
    for x in ("bytes", "KB", "MB", "GB", "TB"):
        if size < 1024.0:
            break
        size /= 1024.0

    return f"{size:.1f} {x}"


def make_thumbnail(img_path: Path, size: tuple[int, int] = (300, 300)) -> bytes:
    """
    Make this image into a captioned thumbnail
    """
    # get a pw
    im = Image.open(img_path)
    pw = im.copy().convert("RGB")
    pw.thumbnail(size=size, resample=Image.Resampling.LANCZOS)

    # make a blank image for the text
    line_height = 16
    pw_with_line = Image.new(
        mode="RGB",
        size=(pw.width, pw.height + line_height),
        color=(255, 255, 255),
    )
    pw_with_line.paste(pw, box=(0, 0))

    # get a file size info
    fsize = img_path.stat().st_size
    fsize_str = human_size(fsize)

    # get font
    font = getenv("THUMB_FONT")
    if font is None:
        font = "arial.ttf"
    fnt = ImageFont.truetype(font, size=14)

    # draw text
    d = ImageDraw.Draw(pw_with_line)
    d.text(
        xy=(pw.width / 5, pw.height),
        text=f"{im.width}x{im.height} ({im.format}) [{fsize_str}]",
        font=fnt,
        fill=(0, 0, 0),
    )

    # save to buffer
    buffer = BytesIO()
    pw_with_line.save(
        buffer,
        format="JPEG",
        quality=95,
        optimize=True,
        progressive=True,
    )

    return buffer.getvalue()


def kdialog(text_to_print: str) -> None:
    """
    Kde notifications
    """
    if kdialog := which("kdialog"):
        Popen([kdialog, "--passivepopup", text_to_print])
