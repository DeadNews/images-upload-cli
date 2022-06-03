#!/usr/bin/env python
"""
Upload images via API
"""
from argparse import ArgumentParser, Namespace
from base64 import b64encode
from io import BytesIO
from os import getenv
from pathlib import Path
from re import search
from shutil import which
from subprocess import Popen
from urllib.parse import urlparse

from dotenv import find_dotenv, load_dotenv
from PIL import Image, ImageDraw, ImageFont
from pyperclip import copy as copy_to_clipboard
from requests import get, post


def parse_args() -> Namespace:
    parser = ArgumentParser(description=__doc__)

    parser.add_argument(
        dest="input_files",
        type=str,
        nargs="+",
        help="Path to the input files",
    )
    parser.add_argument(
        "-s",
        "--server_name",
        type=str.lower,
        choices=(
            "fastpic",
            "freeimage",
            "geekpic",
            "imageban",
            "imageshack",
            "imgbb",
            "imgur",
            "pixhost",
        ),
        default="fastpic",
        help="Hosting for uploading images",
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-b",
        "--bbcode",
        action="store_true",
        default=False,
        help="Add bbcode tags",
    )
    group.add_argument(
        "-t",
        "--thumbnail",
        action="store_true",
        default=False,
        help="Generate thumbnails",
    )

    return parser.parse_args()


def get_env_val(key: str) -> str:
    value = getenv(key)
    if value is None:
        raise Exception(f"Please setup the .env variable {key}.")
    return value


def fastpic_upload(img: bytes) -> str:
    response = post(
        url="https://fastpic.org/upload?api=1",
        data={
            "method": "file",
            "check_thumb": "no",
            "uploading": "1",
        },
        files={"file1": img},
    )

    image_link = (
        None
        if (match := search(r"<imagepath>(.+?)</imagepath>", response.text)) is None
        else match.group(1).strip()
    )
    if image_link is None:
        raise Exception(response.text)

    return image_link


def freeimage_upload(img: bytes) -> str:
    key = get_env_val("FREEIMAGE_KEY")

    response = post(
        url="https://freeimage.host/api/1/upload",
        data={"key": key},
        files={"source": img},
    )
    if not response.ok:
        raise Exception(response.json())

    image_link = response.json()["image"]["url"]

    return image_link


def geekpic_upload(img: bytes) -> str:
    response = post(
        url="https://geekpic.net/client.php",
        data={"image": b64encode(img)},
    )
    if not response.ok:
        raise Exception(response.json())

    image_link = response.json()["link"]

    return image_link


def imageban_upload(img: bytes) -> str:
    token = get_env_val("IMAGEBAN_TOKEN")

    response = post(
        url="https://api.imageban.ru/v1",
        headers={
            "Authorization": f"TOKEN {token}",
        },
        files={"image": img},
    )
    if not response.ok:
        raise Exception(response.json())

    image_link = response.json()["data"]["link"]

    return image_link


def imageshack_upload(img: bytes) -> str:
    key = get_env_val("IMAGESHACK_KEY")

    response = post(
        url="https://post.imageshack.us/upload_api.php",
        data={
            "key": key,
            "format": "json",
        },
        files={"fileupload": img},
    )
    if not response.ok:
        raise Exception(response.json())

    image_link = response.json()["links"]["image_link"]

    return image_link


def imgbb_upload(img: bytes) -> str:
    key = get_env_val("IMGBB_KEY")

    response = post(
        url="https://api.imgbb.com/1/upload",
        data={"key": key},
        files={"image": img},
    )
    if not response.ok:
        raise Exception(response.json())

    image_link = response.json()["data"]["url"]

    return image_link


def imgur_upload(img: bytes) -> str:
    client_id = get_env_val("IMGUR_CLIENT_ID")

    response = post(
        url="https://api.imgur.com/3/image",
        headers={"Authorization": f"Client-ID {client_id}"},
        files={"image": img},
    )
    if not response.ok:
        raise Exception(response.json())

    image_link = response.json()["data"]["link"]

    return image_link


def pixhost_upload(img: bytes) -> str:
    response = post(
        url="https://api.pixhost.to/images",
        data={"content_type": 0},
        files={"img": img},
    )
    if not response.ok:
        raise Exception(response.json())

    show_url = response.json()["show_url"]

    # get direct link
    u = urlparse(show_url)
    match = search(
        rf"({u.scheme}://(.+?){u.netloc}/images/{u.path.removeprefix('/show/')})",
        get(show_url).text,
    )
    image_link = None if match is None else match.group(0).strip()

    return show_url if image_link is None else image_link


def human_size(size: float) -> str:
    """
    This function will convert bytes to MB... GB... etc
    """
    for x in ("bytes", "KB", "MB", "GB", "TB"):
        if size < 1024.0:
            break
        size /= 1024.0

    return f"{size:.1f} {x}"


def make_thumbnail(img_path: Path) -> bytes:
    """
    Make this image into a captioned thumbnail
    """
    # get a pw
    im = Image.open(img_path)
    pw = im.copy().convert("RGB")
    pw.thumbnail(size=(300, 300), resample=Image.Resampling.LANCZOS)

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


if __name__ == "__main__":
    args = parse_args()

    # loading .env variables
    load_dotenv(dotenv_path=find_dotenv())

    # get upload func
    upload = {
        "fastpic": fastpic_upload,
        "freeimage": freeimage_upload,
        "geekpic": geekpic_upload,
        "imageban": imageban_upload,
        "imageshack": imageshack_upload,
        "imgbb": imgbb_upload,
        "imgur": imgur_upload,
        "pixhost": pixhost_upload,
    }
    upload_func = upload[args.server_name]

    # image uploader
    links = []
    for f1 in args.input_files:
        img_path = Path(f1)
        img = img_path.read_bytes()

        if not args.thumbnail:
            link = f"[img]{upload_func(img)}[/img]" if args.bbcode else upload_func(img)
        else:
            thumbnail = make_thumbnail(img_path)
            link = f"[url={upload_func(img)}][img]{upload_func(thumbnail)}[/img][/url]"

        links.append(link)

    # out
    links_str = " ".join(links)
    print(links_str)
    copy_to_clipboard(links_str)
    kdialog(links_str)
