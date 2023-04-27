#!/usr/bin/env python
from __future__ import annotations

from collections.abc import Callable
from os import getenv
from re import DOTALL, search, sub
from urllib.parse import urlparse

from requests import get, post

from images_upload_cli.util import get_env_val, get_img_ext


class UploadError(Exception):
    pass


def beeimg_upload(img: bytes) -> str:
    ext = f"img.{get_img_ext(img)}"

    response = post(
        url="https://beeimg.com/api/upload/file/json/",
        files={"file": (f"img.{ext}", img, f"image/{ext}")},
    )
    if not response.ok:
        raise UploadError(response.json())

    return f"https:{response.json()['files']['url']}"


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


def imagebin_upload(img: bytes) -> str:
    response = post(
        url="https://imagebin.ca/upload.php",
        files={"file": img},
    )
    if not response.ok:
        raise UploadError(response.text)

    return sub(r".*url:", "", response.text, flags=DOTALL)


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
    client_id = getenv("IMGUR_CLIENT_ID", "dd32dd3c6aaa9a0")

    response = post(
        url="https://api.imgur.com/3/image",
        headers={"Authorization": f"Client-ID {client_id}"},
        files={"image": img},
    )
    if not response.ok:
        raise UploadError(response.json())

    return response.json()["data"]["link"]


def lensdump_upload(img: bytes) -> str:
    key = get_env_val("LENSDUMP_KEY")

    response = post(
        url="https://lensdump.com/api/1/upload",
        data={"key": key},
        files={"source": img},
    )
    if not response.ok:
        raise UploadError(response.json())

    print(response.json())

    return response.json()["image"]["url"]


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


def smms_upload(img: bytes) -> str:
    key = get_env_val("SMMS_KEY")

    response = post(
        url="https://sm.ms/api/v2/upload",
        headers={"Authorization": key},
        files={"smfile": img},
    )
    if not response.ok:
        raise UploadError(response.json())

    return (
        response.json()["images"]
        if response.json()["code"] == "image_repeated"
        else response.json()["data"]["url"]
    )


def sxcu_upload(img: bytes) -> str:
    response = post(
        url="https://sxcu.net/api/files/create",
        files={"file": img},
    )
    if not response.ok:
        raise UploadError(response.text)

    return f"{response.json()['url']}.{get_img_ext(img)}"


def telegraph_upload(img: bytes) -> str:
    response = post(
        url="https://telegra.ph/upload",
        files={"file": img},
    )
    if not response.ok:
        raise UploadError(response.json())

    return f"https://telegra.ph{response.json()[0]['src']}"


def thumbsnap_upload(img: bytes) -> str:
    key = get_env_val("THUMBSNAP_KEY")

    response = post(
        url="https://thumbsnap.com/api/upload",
        data={"key": key},
        files={"media": img},
    )
    if not response.ok:
        raise UploadError(response.json())

    return response.json()["data"]["media"]


def up2sha_upload(img: bytes) -> str:
    key = get_env_val("UP2SHA_KEY")
    ext = get_img_ext(img)

    response = post(
        url="https://api.up2sha.re/files",
        headers={"X-Api-Key": key},
        files={"file": (f"img.{ext}", img)},
    )
    if not response.ok:
        raise UploadError(response.json())

    return f"{response.json()['public_url'].replace('file?f=', 'media/raw/')}.{ext}"


def uplio_upload(img: bytes) -> str:
    key = get_env_val("UPLIO_KEY")
    ext = get_img_ext(img)

    response = post(
        url="https://upl.io",
        data={"key": key},
        files={"file": (f"img.{ext}", img)},
    )
    if not response.ok:
        raise UploadError(response.text)

    host, uid = response.text.rsplit("/", 1)
    return f"{host}/i/{uid}.{ext}"


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


def vgy_upload(img: bytes) -> str:
    key = get_env_val("VGY_KEY")
    name = f"img.{get_img_ext(img)}"

    response = post(
        url="https://vgy.me/upload",
        data={"userkey": key},
        files={"file[]": (name, img)},
    )
    if not response.ok:
        raise UploadError(response.json())

    return response.json()["image"]


UPLOAD: dict[str, Callable[[bytes], str]] = {
    "beeimg": beeimg_upload,
    "catbox": catbox_upload,
    "fastpic": fastpic_upload,
    "filecoffee": filecoffee_upload,
    "freeimage": freeimage_upload,
    "gyazo": gyazo_upload,
    "imageban": imageban_upload,
    "imagebin": imagebin_upload,
    "imgbb": imgbb_upload,
    "imgchest": imgchest_upload,
    "imgur": imgur_upload,
    "lensdump": lensdump_upload,
    "pictshare": pictshare_upload,
    "pixeldrain": pixeldrain_upload,
    "pixhost": pixhost_upload,
    "ptpimg": ptpimg_upload,
    "smms": smms_upload,
    "sxcu": sxcu_upload,
    "telegraph": telegraph_upload,
    "thumbsnap": thumbsnap_upload,
    "up2sha": up2sha_upload,
    "uplio": uplio_upload,
    "uploadcare": uploadcare_upload,
    "vgy": vgy_upload,
}

HOSTINGS = tuple(UPLOAD.keys())
