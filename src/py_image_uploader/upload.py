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


def catbox_upload(img: bytes) -> str:
    response = post(
        url="https://catbox.moe/user/api.php",
        data={"reqtype": "fileupload"},
        files={"fileToUpload": img},
    )
    if not response.ok:
        raise UploadError(response.text)

    return f"{response.text}"


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


def filecoffee_upload(img: bytes) -> str:
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
        files={"imagedata": ("img.png", img)},
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


def imgchest_upload(img: bytes) -> str:
    key = get_env_val("IMGCHEST_KEY")
    name = f"img.{get_img_ext(img)}"

    response = post(
        url="https://api.imgchest.com/v1/post",
        headers={"Authorization": f"Bearer {key}"},
        files={"images[]": (name, img)},
    )
    if not response.ok:
        raise UploadError(response.json())

    return response.json()["data"]["images"][0]["link"].replace("comfiles", "com/files")


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


def pictshare_upload(img: bytes) -> str:
    response = post(
        url="https://pictshare.net/api/upload.php",
        files={"file": img},
    )
    if not response.ok:
        raise UploadError(response.json())

    return response.json()["url"]


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


def ptpimg_upload(img: bytes) -> str:
    key = get_env_val("PTPIMG_KEY")

    response = post(
        url="https://ptpimg.me/upload.php",
        data={"api_key": key},
        files={"file-upload[0]": img},
    )
    if not response.ok:
        raise UploadError(response.json())

    return f"https://ptpimg.me/{response.json()[0]['code']}.{response.json()[0]['ext']}"


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
        files={"filename": (name, img)},
    )
    if not response.ok:
        raise UploadError(response.json())

    return f"https://ucarecdn.com/{response.json()['filename']}/{name}"


UPLOAD: dict[str, Callable[[bytes], str]] = {
    "catbox": catbox_upload,
    "fastpic": fastpic_upload,
    "filecoffee": filecoffee_upload,
    "freeimage": freeimage_upload,
    "geekpic": geekpic_upload,
    "gyazo": gyazo_upload,
    "imageban": imageban_upload,
    "imgbb": imgbb_upload,
    "imgchest": imgchest_upload,
    "imgur": imgur_upload,
    "pictshare": pictshare_upload,
    "pixeldrain": pixeldrain_upload,
    "pixhost": pixhost_upload,
    "ptpimg": ptpimg_upload,
    "up2sha": up2sha_upload,
    "uploadcare": uploadcare_upload,
}


HOSTINGS = tuple(UPLOAD.keys())
