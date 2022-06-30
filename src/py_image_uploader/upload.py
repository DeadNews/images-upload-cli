#!/usr/bin/env python
from __future__ import annotations

from base64 import b64encode
from re import search
from typing import Callable
from urllib.parse import urlparse

from requests import get, post

from .util import get_env_val


class InvalidParameterError(Exception):
    pass


class UploadError(Exception):
    pass


def get_upload_func(server_name: str) -> Callable[[bytes], str]:
    """
    Get function by server name
    """
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

    if server_name not in (keys := list(upload.keys())):
        raise InvalidParameterError(
            f"Invalid parameter {server_name=}. Expected one of {keys}."
        )

    return upload[server_name]


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
        raise UploadError(response.text)

    return image_link


def freeimage_upload(img: bytes) -> str:
    key = get_env_val("FREEIMAGE_KEY")

    response = post(
        url="https://freeimage.host/api/1/upload",
        data={"key": key},
        files={"source": img},
    )
    if not response.ok:
        raise UploadError(response.json())

    image_link = response.json()["image"]["url"]

    return image_link


def geekpic_upload(img: bytes) -> str:
    response = post(
        url="https://geekpic.net/client.php",
        data={"image": b64encode(img)},
    )
    if not response.ok:
        raise UploadError(response.json())

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
        raise UploadError(response.json())

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
        raise UploadError(response.json())

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
        raise UploadError(response.json())

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
        raise UploadError(response.json())

    image_link = response.json()["data"]["link"]

    return image_link


def pixhost_upload(img: bytes) -> str:
    response = post(
        url="https://api.pixhost.to/images",
        data={"content_type": 0},
        files={"img": img},
    )
    if not response.ok:
        raise UploadError(response.json())

    show_url = response.json()["show_url"]

    # get direct link
    u = urlparse(show_url)
    match = search(
        rf"({u.scheme}://(.+?){u.netloc}/images/{u.path.removeprefix('/show/')})",
        get(show_url).text,
    )
    image_link = None if match is None else match.group(0).strip()

    return show_url if image_link is None else image_link
