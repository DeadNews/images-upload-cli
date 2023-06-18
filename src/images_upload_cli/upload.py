#!/usr/bin/env python
"""Upload callables."""
from __future__ import annotations

from os import getenv
from re import DOTALL, search, sub
from typing import TYPE_CHECKING
from urllib.parse import urlparse

from httpx import AsyncClient, HTTPError

from images_upload_cli.util import get_env, get_img_ext

if TYPE_CHECKING:
    from collections.abc import Callable


async def beeimg_upload(client: AsyncClient, img: bytes) -> str:
    """Upload to beeimg.com."""
    ext = f"img.{get_img_ext(img)}"

    response = await client.post(
        url="https://beeimg.com/api/upload/file/json/",
        files={"file": (f"img.{ext}", img, f"image/{ext}")},
    )
    response.raise_for_status()

    return f"https:{response.json()['files']['url']}"


async def catbox_upload(client: AsyncClient, img: bytes) -> str:
    """Upload to catbox.moe."""
    response = await client.post(
        url="https://catbox.moe/user/api.php",
        data={"reqtype": "fileupload"},
        files={"fileToUpload": img},
    )
    response.raise_for_status()

    return f"{response.text}"


async def fastpic_upload(client: AsyncClient, img: bytes) -> str:
    """Upload to fastpic.org."""
    response = await client.post(
        url="https://fastpic.org/upload?api=1",
        data={
            "method": "file",
            "check_thumb": "no",
            "uploading": "1",
        },
        files={"file1": img},
    )
    response.raise_for_status()

    match = search(r"<imagepath>(.+?)</imagepath>", response.text)
    if match is None:
        msg = "Link not found in response."
        raise HTTPError(msg)

    return match.group(1).strip()


async def filecoffee_upload(client: AsyncClient, img: bytes) -> str:
    """Upload to file.coffee."""
    response = await client.post(
        url="https://file.coffee/api/file/upload",
        files={"file": img},
    )
    response.raise_for_status()

    return response.json()["url"]


async def freeimage_upload(client: AsyncClient, img: bytes) -> str:
    """Upload to freeimage.host."""
    key = get_env("FREEIMAGE_KEY")

    response = await client.post(
        url="https://freeimage.host/api/1/upload",
        data={"key": key},
        files={"source": img},
    )
    response.raise_for_status()

    return response.json()["image"]["url"]


async def gyazo_upload(client: AsyncClient, img: bytes) -> str:
    """Upload to gyazo.com."""
    key = get_env("GYAZO_TOKEN")

    response = await client.post(
        url=f"https://upload.gyazo.com/api/upload?access_token={key}",
        files={"imagedata": img},
    )
    response.raise_for_status()

    return response.json()["url"]


async def imageban_upload(client: AsyncClient, img: bytes) -> str:
    """Upload to imageban.ru."""
    token = get_env("IMAGEBAN_TOKEN")

    response = await client.post(
        url="https://api.imageban.ru/v1",
        headers={"Authorization": f"TOKEN {token}"},
        files={"image": img},
    )
    response.raise_for_status()

    return response.json()["data"]["link"]


async def imagebin_upload(client: AsyncClient, img: bytes) -> str:
    """Upload to imagebin.ca."""
    response = await client.post(
        url="https://imagebin.ca/upload.php",
        files={"file": img},
    )
    response.raise_for_status()

    return sub(r".*url:", "", response.text, flags=DOTALL)


async def imgbb_upload(client: AsyncClient, img: bytes) -> str:
    """Upload to imgbb.com."""
    key = get_env("IMGBB_KEY")

    response = await client.post(
        url="https://api.imgbb.com/1/upload",
        data={"key": key},
        files={"image": img},
    )
    response.raise_for_status()

    return response.json()["data"]["url"]


async def imgchest_upload(client: AsyncClient, img: bytes) -> str:
    """Upload to imgchest.com."""
    key = get_env("IMGCHEST_KEY")
    ext = get_img_ext(img)

    response = await client.post(
        url="https://api.imgchest.com/v1/post",
        headers={"Authorization": f"Bearer {key}"},
        files={"images[]": (f"img.{ext}", img)},
    )
    response.raise_for_status()

    return response.json()["data"]["images"][0]["link"].replace("comfiles", "com/files")


async def imgur_upload(client: AsyncClient, img: bytes) -> str:
    """Upload to imgur.com."""
    client_id = getenv("IMGUR_CLIENT_ID", "dd32dd3c6aaa9a0")

    response = await client.post(
        url="https://api.imgur.com/3/image",
        headers={"Authorization": f"Client-ID {client_id}"},
        files={"image": img},
    )
    response.raise_for_status()

    return response.json()["data"]["link"]


async def lensdump_upload(client: AsyncClient, img: bytes) -> str:
    """Upload to lensdump.com."""
    key = get_env("LENSDUMP_KEY")

    response = await client.post(
        url="https://lensdump.com/api/1/upload",
        data={"key": key},
        files={"source": img},
    )
    response.raise_for_status()

    return response.json()["image"]["url"]


async def pictshare_upload(client: AsyncClient, img: bytes) -> str:
    """Upload to pictshare.net."""
    response = await client.post(
        url="https://pictshare.net/api/upload.php",
        files={"file": img},
    )
    response.raise_for_status()

    return response.json()["url"]


async def pixeldrain_upload(client: AsyncClient, img: bytes) -> str:
    """Upload to pixeldrain.com."""
    response = await client.post(
        url="https://pixeldrain.com/api/file",
        files={"file": img},
    )
    response.raise_for_status()

    return f"https://pixeldrain.com/api/file/{response.json()['id']}"


async def pixhost_upload(client: AsyncClient, img: bytes) -> str:
    """Upload to pixhost.to."""
    response = await client.post(
        url="https://api.pixhost.to/images",
        data={"content_type": 0},
        files={"img": img},
    )
    response.raise_for_status()

    show_url = response.json()["show_url"]

    # get direct link
    get_resp = await client.get(show_url)
    u = urlparse(show_url)
    match = search(
        rf"({u.scheme}://(.+?){u.netloc}/images/{u.path.removeprefix('/show/')})",
        get_resp.text,
    )
    image_link = None if match is None else match.group(0).strip()

    return show_url if image_link is None else image_link


async def ptpimg_upload(client: AsyncClient, img: bytes) -> str:
    """Upload to ptpimg.me."""
    key = get_env("PTPIMG_KEY")

    response = await client.post(
        url="https://ptpimg.me/upload.php",
        data={"api_key": key},
        files={"file-upload[0]": img},
    )
    response.raise_for_status()

    return f"https://ptpimg.me/{response.json()[0]['code']}.{response.json()[0]['ext']}"


async def smms_upload(client: AsyncClient, img: bytes) -> str:
    """Upload to sm.ms."""
    key = get_env("SMMS_KEY")

    response = await client.post(
        url="https://sm.ms/api/v2/upload",
        headers={"Authorization": key},
        files={"smfile": img},
    )
    response.raise_for_status()

    return (
        response.json()["images"]
        if response.json()["code"] == "image_repeated"
        else response.json()["data"]["url"]
    )


async def sxcu_upload(client: AsyncClient, img: bytes) -> str:
    """Upload to sxcu.net."""
    response = await client.post(
        url="https://sxcu.net/api/files/create",
        files={"file": img},
    )
    response.raise_for_status()

    return f"{response.json()['url']}.{get_img_ext(img)}"


async def telegraph_upload(client: AsyncClient, img: bytes) -> str:
    """Upload to telegra.ph."""
    response = await client.post(
        url="https://telegra.ph/upload",
        files={"file": img},
    )
    response.raise_for_status()

    return f"https://telegra.ph{response.json()[0]['src']}"


async def thumbsnap_upload(client: AsyncClient, img: bytes) -> str:
    """Upload to thumbsnap.com."""
    key = get_env("THUMBSNAP_KEY")

    response = await client.post(
        url="https://thumbsnap.com/api/upload",
        data={"key": key},
        files={"media": img},
    )
    response.raise_for_status()

    return response.json()["data"]["media"]


async def tixte_upload(client: AsyncClient, img: bytes) -> str:
    """Upload to tixte.com."""
    key = get_env("TIXTE_KEY")
    ext = get_img_ext(img)

    response = await client.post(
        url="https://api.tixte.com/v1/upload",
        headers={"Authorization": key},
        data={"payload_json": '{"random":true}'},
        files={"file": (f"img.{ext}", img)},
    )
    response.raise_for_status()

    return response.json()["data"]["direct_url"]


async def up2sha_upload(client: AsyncClient, img: bytes) -> str:
    """Upload to up2sha.re."""
    key = get_env("UP2SHA_KEY")
    ext = get_img_ext(img)

    response = await client.post(
        url="https://api.up2sha.re/files",
        headers={"X-Api-Key": key},
        files={"file": (f"img.{ext}", img)},
    )
    response.raise_for_status()

    return f"{response.json()['public_url'].replace('file?f=', 'media/raw/')}.{ext}"


async def uplio_upload(client: AsyncClient, img: bytes) -> str:
    """Upload to upl.io."""
    key = get_env("UPLIO_KEY")
    ext = get_img_ext(img)

    response = await client.post(
        url="https://upl.io",
        data={"key": key},
        files={"file": (f"img.{ext}", img)},
    )
    response.raise_for_status()

    host, uid = response.text.rsplit("/", 1)
    return f"{host}/i/{uid}.{ext}"


async def uploadcare_upload(client: AsyncClient, img: bytes) -> str:
    """Upload to uploadcare.com."""
    key = get_env("UPLOADCARE_KEY")
    name = f"img.{get_img_ext(img)}"

    response = await client.post(
        url="https://upload.uploadcare.com/base/",
        data={
            "UPLOADCARE_PUB_KEY": key,
            "UPLOADCARE_STORE": "1",
        },
        files={"filename": (name, img)},
    )
    response.raise_for_status()

    return f"https://ucarecdn.com/{response.json()['filename']}/{name}"


async def vgy_upload(client: AsyncClient, img: bytes) -> str:
    """Upload to vgy.me."""
    key = get_env("VGY_KEY")
    ext = get_img_ext(img)

    response = await client.post(
        url="https://vgy.me/upload",
        data={"userkey": key},
        files={"file[]": (f"img.{ext}", img)},
    )
    response.raise_for_status()

    return response.json()["image"]


UPLOAD: dict[str, Callable] = {
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
    "tixte": tixte_upload,
    "up2sha": up2sha_upload,
    "uplio": uplio_upload,
    "uploadcare": uploadcare_upload,
    "vgy": vgy_upload,
}

HOSTINGS = tuple(UPLOAD.keys())
