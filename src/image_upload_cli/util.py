#!/usr/bin/env python
from __future__ import annotations

from io import BytesIO
from os import getenv
from pathlib import Path
from platform import system
from shutil import which
from subprocess import Popen

import click
from PIL import Image, ImageDraw, ImageFont


class GetenvError(Exception):
    pass


def get_config_path() -> Path:
    """
    Get app config path.
    """
    return Path(f"{click.get_app_dir('image-upload-cli')}/.env")


def get_env_val(key: str) -> str:
    """
    Get value from env.
    """
    if value := getenv(key):
        return value
    else:
        raise GetenvError(
            f"Please setup {key} in environment variables or in '{get_config_path()}'"
        )


def human_size(num: float, suffix: str = "B") -> str:
    """
    This function will convert bytes to human readable units.
    """
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f} {unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f} Yi{suffix}"


def get_img_ext(img: bytes) -> str:
    """
    Get image extension from bytes.
    """
    return Image.open(BytesIO(img)).format.lower()


def get_font() -> str | None:
    """
    Attempts to retrieve a reasonably-looking TTF font from the system.

    We don't make much of an effort, but it's what we can reasonably do without
    incorporating additional dependencies for this task.
    """
    if system == "Windows":
        font_names = ["Arial"]
    elif system == "Linux":
        font_names = ["DejaVuSans-Bold", "DroidSans-Bold"]
    elif system == "Darwin":
        font_names = ["Helvetica", "Menlo"]

    font = None
    for font_name in font_names:
        try:
            font = ImageFont.truetype(font_name)
            break
        except IOError:
            continue

    return font


def make_thumbnail(img: bytes, size: tuple[int, int] = (300, 300)) -> bytes:
    """
    Make this image into a captioned thumbnail.
    """
    # get a pw
    im = Image.open(BytesIO(img))
    pw = im.copy().convert("RGB")
    pw.thumbnail(size=size, resample=Image.Resampling.LANCZOS)

    # make a blank image for the text
    pw_with_line = Image.new(
        mode="RGB",
        size=(pw.width, pw.height + 16),
        color=(255, 255, 255),
    )
    pw_with_line.paste(pw, box=(0, 0))

    # get a file size info
    fsize = human_size(len(img))

    # get font
    font = getenv("CAPTION_FONT")
    if not font:
        fnt = get_font()

    fnt = ImageFont.truetype(font, size=14)

    # draw text
    d = ImageDraw.Draw(pw_with_line)
    d.text(
        xy=(pw.width / 5, pw.height),
        text=f"{im.width}x{im.height} ({im.format}) [{fsize}]",
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
    Kde notifications.
    """
    if kdialog := which("kdialog"):
        Popen([kdialog, "--passivepopup", text_to_print])
