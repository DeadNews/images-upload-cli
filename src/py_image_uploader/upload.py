#!/usr/bin/env python
from __future__ import annotations

from base64 import b64encode
from collections.abc import Callable
from re import search
from urllib.parse import urlparse

from requests import get, post

from .util import get_env_val, get_img_ext


class UploadError(Exception):
    pass


def test_upload(img: bytes) -> str:
    # key = get_env_val("GYAZO_TOKEN")

    response = post(
        url="https://api.anonfiles.com/upload",
        # data={
        #     "reqtype": "fileupload",
        #     "image": b64encode(img),
        # },
        files={"file": img},
    )
    if not response.ok:
        raise UploadError(response.json())

    print(response.json())

    return "test"


def beeimg_upload(img: bytes) -> str:
    key = get_env_val("BEEIMG_KEY")

    response = post(
        url="https://beeimg.com/api/upload/file/json/",
        headers={"apikey": key},
        files={"image": img},
    )
    if not response.ok:
        raise UploadError(response.json())

    print(response.json())

    return f"https:{response.json()['files']['url']}"


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


def file_coffee_upload(img: bytes) -> str:
    response = post(
        url="https://file.coffee/api/file/upload",
        files={"file": img},
    )
    if not response.ok:
        raise UploadError(response.json())

    return response.json()["url"]


def freeimage_upload(img: bytes) -> str:
    key = get_env_val("FREEIMAGE_KEY")

    response = post(
        url="https://freeimage.host/api/1/upload",
        data={"key": key},
        files={"source": img},
    )
    if not response.ok:
        raise UploadError(response.json())

    return response.json()["image"]["url"]


def geekpic_upload(img: bytes) -> str:
    response = post(
        url="https://geekpic.net/client.php",
        data={"image": b64encode(img)},
    )
    if not response.ok:
        raise UploadError(response.json())

    return response.json()["link"]


def gyazo_upload(img: bytes) -> str:
    key = get_env_val("GYAZO_TOKEN")

    response = post(
        url=f"https://upload.gyazo.com/api/upload?access_token={key}",
        files={"imagedata": img},
    )
    if not response.ok:
        raise UploadError(response.json())

    return response.json()["url"]


def imageban_upload(img: bytes) -> str:
    token = get_env_val("IMAGEBAN_TOKEN")

    response = post(
        url="https://api.imageban.ru/v1",
        headers={"Authorization": f"TOKEN {token}"},
        files={"image": img},
    )
    if not response.ok:
        raise UploadError(response.json())

    return response.json()["data"]["link"]


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

    return response.json()["links"]["image_link"]


def imgbb_upload(img: bytes) -> str:
    key = get_env_val("IMGBB_KEY")

    response = post(
        url="https://api.imgbb.com/1/upload",
        data={"key": key},
        files={"image": img},
    )
    if not response.ok:
        raise UploadError(response.json())

    return response.json()["data"]["url"]


def imgur_upload(img: bytes) -> str:
    client_id = get_env_val("IMGUR_CLIENT_ID")

    response = post(
        url="https://api.imgur.com/3/image",
        headers={"Authorization": f"Client-ID {client_id}"},
        files={"image": img},
    )
    if not response.ok:
        raise UploadError(response.json())

    return response.json()["data"]["link"]


def pixeldrain_upload(img: bytes) -> str:
    response = post(
        url="https://pixeldrain.com/api/file",
        files={"file": img},
    )
    if not response.ok:
        raise UploadError(response.json())

    return f"https://pixeldrain.com/api/file/{response.json()['id']}"


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


def up2sha_upload(img: bytes) -> str:
    key = get_env_val("UP2SHA_KEY")
    ext = get_img_ext(img)

    response = post(
        url="https://api.up2sha.re/files",
        headers={"X-Api-Key": key},
        data={"filename": f"img.{ext}"},
        files={"file": img},
    )
    if not response.ok:
        raise UploadError(response.json())

    return f"{response.json()['public_url'].replace('file?f=', 'media/raw/')}.{ext}"


def uploadcare_upload(img: bytes) -> str:
    key = get_env_val("UPLOADCARE_KEY")
    name = f"img.{get_img_ext(img)}"

    response = post(
        url="https://upload.uploadcare.com/base/",
        data={
            "UPLOADCARE_PUB_KEY": key,
            "UPLOADCARE_STORE": "1",
        },
        files={name: img},
    )
    if not response.ok:
        raise UploadError(response.json())

    return f"https://ucarecdn.com/{response.json()[name]}/{name}"


UPLOAD: dict[str, Callable[[bytes], str]] = {
    "beeimg": beeimg_upload,
    "fastpic": fastpic_upload,
    "file_coffee": file_coffee_upload,
    "freeimage": freeimage_upload,
    "geekpic": geekpic_upload,
    "gyazo": gyazo_upload,
    "imageban": imageban_upload,
    "imageshack": imageshack_upload,
    "imgbb": imgbb_upload,
    "imgur": imgur_upload,
    "pixeldrain": pixeldrain_upload,
    "pixhost": pixhost_upload,
    "test": test_upload,
    "up2sha": up2sha_upload,
    "uploadcare": uploadcare_upload,
    # https://ptpimg.me
}


HOSTINGS = tuple(UPLOAD.keys())
