"""Upload callables."""

from collections.abc import Callable
from os import getenv
from re import search
from urllib.parse import urlparse

from httpx import AsyncClient, HTTPError

from images_upload_cli.util import get_env, get_img_ext


async def anhmoe_upload(client: AsyncClient, img: bytes) -> str:
    """
    Uploads an image to the `anh.moe`.

    Args:
        client (httpx.AsyncClient): An instance of AsyncClient.
        img (bytes): A byte string representing an image.

    Returns:
        str: The URL of the uploaded image.

    Raises:
        httpx.HTTPStatusError: If the response status code is not successful.
    """
    key = "anh.moe_public_api"

    response = await client.post(
        url="https://anh.moe/api/1/upload",
        data={"key": key},
        files={"source": img},
    )
    response.raise_for_status()

    return response.json()["image"]["url"]


async def beeimg_upload(client: AsyncClient, img: bytes) -> str:
    """
    Uploads an image to the `beeimg.com`.

    Args:
        client (httpx.AsyncClient): An instance of AsyncClient.
        img (bytes): A byte string representing an image.

    Returns:
        str: The URL of the uploaded image.

    Raises:
        httpx.HTTPStatusError: If the response status code is not successful.
    """
    ext = get_img_ext(img)
    name = f"img.{ext}"
    content_type = f"image/{ext}"

    response = await client.post(
        url="https://beeimg.com/api/upload/file/json/",
        files={"file": (name, img, content_type)},
    )
    response.raise_for_status()

    return f"https:{response.json()['files']['url']}"


async def catbox_upload(client: AsyncClient, img: bytes) -> str:
    """
    Uploads an image to the `catbox.moe`.

    Args:
        client (httpx.AsyncClient): An instance of AsyncClient.
        img (bytes): A byte string representing an image.

    Returns:
        str: The URL of the uploaded image.

    Raises:
        httpx.HTTPStatusError: If the response status code is not successful.
    """
    response = await client.post(
        url="https://catbox.moe/user/api.php",
        data={"reqtype": "fileupload"},
        files={"fileToUpload": img},
    )
    response.raise_for_status()

    return response.text


async def fastpic_upload(client: AsyncClient, img: bytes) -> str:
    """
    Uploads an image to the `fastpic.org`.

    Args:
        client (httpx.AsyncClient): An instance of AsyncClient.
        img (bytes): A byte string representing an image.

    Returns:
        str: The URL of the uploaded image.

    Raises:
        httpx.HTTPStatusError: If the response status code is not successful.
        httpx.HTTPError: If the image link is not found in the response.
    """
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
        msg = f"Image link not found in '{response.url}' response:\n\n{response.text}"
        raise HTTPError(msg)

    return match[1].strip()


async def filecoffee_upload(client: AsyncClient, img: bytes) -> str:
    """
    Uploads an image to the `file.coffee`.

    Args:
        client (httpx.AsyncClient): An instance of AsyncClient.
        img (bytes): A byte string representing an image.

    Returns:
        str: The URL of the uploaded image.

    Raises:
        httpx.HTTPStatusError: If the response status code is not successful.
    """
    response = await client.post(
        url="https://file.coffee/api/file/upload",
        files={"file": img},
    )
    response.raise_for_status()

    return response.json()["url"]


async def freeimage_upload(client: AsyncClient, img: bytes) -> str:
    """
    Uploads an image to the `freeimage.host`.

    Args:
        client (httpx.AsyncClient): An instance of AsyncClient.
        img (bytes): A byte string representing an image.

    Returns:
        str: The URL of the uploaded image.

    Raises:
        httpx.HTTPStatusError: If the response status code is not successful.
    """
    key = get_env("FREEIMAGE_KEY")

    response = await client.post(
        url="https://freeimage.host/api/1/upload",
        data={"key": key},
        files={"source": img},
    )
    response.raise_for_status()

    return response.json()["image"]["url"]


async def gyazo_upload(client: AsyncClient, img: bytes) -> str:
    """
    Uploads an image to the `gyazo.com`.

    Args:
        client (httpx.AsyncClient): An instance of AsyncClient.
        img (bytes): A byte string representing an image.

    Returns:
        str: The URL of the uploaded image.

    Raises:
        httpx.HTTPStatusError: If the response status code is not successful.
    """
    key = get_env("GYAZO_TOKEN")

    response = await client.post(
        url=f"https://upload.gyazo.com/api/upload?access_token={key}",
        files={"imagedata": img},
    )
    response.raise_for_status()

    return response.json()["url"]


async def imageban_upload(client: AsyncClient, img: bytes) -> str:
    """
    Uploads an image to the `imageban.ru`.

    Args:
        client (httpx.AsyncClient): An instance of AsyncClient.
        img (bytes): A byte string representing an image.

    Returns:
        str: The URL of the uploaded image.

    Raises:
        httpx.HTTPStatusError: If the response status code is not successful.
    """
    token = get_env("IMAGEBAN_TOKEN")

    response = await client.post(
        url="https://api.imageban.ru/v1",
        headers={"Authorization": f"TOKEN {token}"},
        files={"image": img},
    )
    response.raise_for_status()

    return response.json()["data"]["link"]


async def imagebin_upload(client: AsyncClient, img: bytes) -> str:
    """
    Uploads an image to the `imagebin.ca`.

    Args:
        client (httpx.AsyncClient): An instance of AsyncClient.
        img (bytes): A byte string representing an image.

    Returns:
        str: The URL of the uploaded image.

    Raises:
        httpx.HTTPStatusError: If the response status code is not successful.
        httpx.HTTPError: If the image link is not found in the response.
    """
    response = await client.post(
        url="https://imagebin.ca/upload.php",
        files={"file": img},
    )
    response.raise_for_status()

    match = search(r"url:(.+?)$", response.text)
    if match is None:
        msg = f"Image link not found in '{response.url}' response:\n\n{response.text}"
        raise HTTPError(msg)

    return match[1].strip()


async def imgbb_upload(client: AsyncClient, img: bytes) -> str:
    """
    Uploads an image to the `imgbb.com`.

    Args:
        client (httpx.AsyncClient): An instance of AsyncClient.
        img (bytes): A byte string representing an image.

    Returns:
        str: The URL of the uploaded image.

    Raises:
        httpx.HTTPStatusError: If the response status code is not successful.
    """
    key = get_env("IMGBB_KEY")

    response = await client.post(
        url="https://api.imgbb.com/1/upload",
        data={"key": key},
        files={"image": img},
    )
    response.raise_for_status()

    return response.json()["data"]["url"]


async def imgchest_upload(client: AsyncClient, img: bytes) -> str:
    """
    Uploads an image to the `imgchest.com`.

    Args:
        client (httpx.AsyncClient): An instance of AsyncClient.
        img (bytes): A byte string representing an image.

    Returns:
        str: The URL of the uploaded image.

    Raises:
        httpx.HTTPStatusError: If the response status code is not successful.
    """
    key = get_env("IMGCHEST_KEY")
    name = f"img.{get_img_ext(img)}"

    response = await client.post(
        url="https://api.imgchest.com/v1/post",
        headers={"Authorization": f"Bearer {key}"},
        files={"images[]": (name, img)},
    )
    response.raise_for_status()

    return response.json()["data"]["images"][0]["link"]


async def imgur_upload(client: AsyncClient, img: bytes) -> str:
    """
    Uploads an image to the `imgur.com`.

    Args:
        client (httpx.AsyncClient): An instance of AsyncClient.
        img (bytes): A byte string representing an image.

    Returns:
        str: The URL of the uploaded image.

    Raises:
        httpx.HTTPStatusError: If the response status code is not successful.
    """
    client_id = getenv("IMGUR_CLIENT_ID", "dd32dd3c6aaa9a0")

    response = await client.post(
        url="https://api.imgur.com/3/image",
        headers={"Authorization": f"Client-ID {client_id}"},
        files={"image": img},
    )
    response.raise_for_status()

    return response.json()["data"]["link"]


async def lensdump_upload(client: AsyncClient, img: bytes) -> str:
    """
    Uploads an image to the `lensdump.com`.

    Args:
        client (httpx.AsyncClient): An instance of AsyncClient.
        img (bytes): A byte string representing an image.

    Returns:
        str: The URL of the uploaded image.

    Raises:
        httpx.HTTPStatusError: If the response status code is not successful.
    """
    key = get_env("LENSDUMP_KEY")

    response = await client.post(
        url="https://lensdump.com/api/1/upload",
        data={"key": key},
        files={"source": img},
    )
    response.raise_for_status()

    return response.json()["image"]["url"]


async def pixeldrain_upload(client: AsyncClient, img: bytes) -> str:
    """
    Uploads an image to the `pixeldrain.com`.

    Args:
        client (httpx.AsyncClient): An instance of AsyncClient.
        img (bytes): A byte string representing an image.

    Returns:
        str: The URL of the uploaded image.

    Raises:
        httpx.HTTPStatusError: If the response status code is not successful.
    """
    response = await client.post(
        url="https://pixeldrain.com/api/file",
        files={"file": img},
    )
    response.raise_for_status()

    return f"https://pixeldrain.com/api/file/{response.json()['id']}"


async def pixhost_upload(client: AsyncClient, img: bytes) -> str:
    """
    Uploads an image to the `pixhost.to`.

    Args:
        client (httpx.AsyncClient): An instance of AsyncClient.
        img (bytes): A byte string representing an image.

    Returns:
        str: The URL of the uploaded image.

    Raises:
        httpx.HTTPStatusError: If the response status code is not successful.
    """
    response = await client.post(
        url="https://api.pixhost.to/images",
        data={"content_type": 0},
        files={"img": img},
    )
    response.raise_for_status()

    show_url = response.json()["show_url"]

    # Get direct link.
    get_resp = await client.get(show_url)
    u = urlparse(show_url)
    match = search(
        rf"({u.scheme}://(.+?){u.netloc}/images/{u.path.removeprefix('/show/')})",
        get_resp.text,
    )
    image_link = None if match is None else match[0].strip()

    return show_url if image_link is None else image_link


async def ptpimg_upload(client: AsyncClient, img: bytes) -> str:
    """
    Uploads an image to the `ptpimg.me`.

    Args:
        client (httpx.AsyncClient): An instance of AsyncClient.
        img (bytes): A byte string representing an image.

    Returns:
        str: The URL of the uploaded image.

    Raises:
        httpx.HTTPStatusError: If the response status code is not successful.
    """
    key = get_env("PTPIMG_KEY")

    response = await client.post(
        url="https://ptpimg.me/upload.php",
        data={"api_key": key},
        files={"file-upload[0]": img},
    )
    response.raise_for_status()

    return f"https://ptpimg.me/{response.json()[0]['code']}.{response.json()[0]['ext']}"


async def smms_upload(client: AsyncClient, img: bytes) -> str:
    """
    Uploads an image to the `sm.ms`.

    Args:
        client (httpx.AsyncClient): An instance of AsyncClient.
        img (bytes): A byte string representing an image.

    Returns:
        str: The URL of the uploaded image.

    Raises:
        httpx.HTTPStatusError: If the response status code is not successful.
    """
    key = get_env("SMMS_KEY")

    response = await client.post(
        url="https://sm.ms/api/v2/upload",
        headers={"Authorization": key},
        files={"smfile": img},
    )
    response.raise_for_status()
    json = response.json()

    return json["images"] if json["code"] == "image_repeated" else json["data"]["url"]


async def sxcu_upload(client: AsyncClient, img: bytes) -> str:
    """
    Uploads an image to the `sxcu.net`.

    Args:
        client (httpx.AsyncClient): An instance of AsyncClient.
        img (bytes): A byte string representing an image.

    Returns:
        str: The URL of the uploaded image.

    Raises:
        httpx.HTTPStatusError: If the response status code is not successful.
    """
    response = await client.post(
        url="https://sxcu.net/api/files/create",
        headers={"user-agent": "python-https/1.0.0"},
        files={"file": img},
    )
    response.raise_for_status()

    return f"{response.json()['url']}.{get_img_ext(img)}"


async def telegraph_upload(client: AsyncClient, img: bytes) -> str:
    """
    Uploads an image to the `telegra.ph`.

    Args:
        client (httpx.AsyncClient): An instance of AsyncClient.
        img (bytes): A byte string representing an image.

    Returns:
        str: The URL of the uploaded image.

    Raises:
        httpx.HTTPStatusError: If the response status code is not successful.
    """
    response = await client.post(
        url="https://telegra.ph/upload",
        files={"file": img},
    )
    response.raise_for_status()

    return f"https://telegra.ph{response.json()[0]['src']}"


async def thumbsnap_upload(client: AsyncClient, img: bytes) -> str:
    """
    Uploads an image to the `thumbsnap.com`.

    Args:
        client (httpx.AsyncClient): An instance of AsyncClient.
        img (bytes): A byte string representing an image.

    Returns:
        str: The URL of the uploaded image.

    Raises:
        httpx.HTTPStatusError: If the response status code is not successful.
    """
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
    """
    Uploads an image to the `freeimage.host`.

    Args:
        client (httpx.AsyncClient): An instance of AsyncClient.
        img (bytes): A byte string representing an image.

    Returns:
        str: The URL of the uploaded image.

    Raises:
        httpx.HTTPStatusError: If the response status code is not successful.
    """
    key = get_env("TIXTE_KEY")
    name = f"img.{get_img_ext(img)}"

    response = await client.post(
        url="https://api.tixte.com/v1/upload",
        headers={"Authorization": key},
        data={"payload_json": '{"random":true}'},
        files={"file": (name, img)},
    )
    response.raise_for_status()

    return response.json()["data"]["direct_url"]


async def up2sha_upload(client: AsyncClient, img: bytes) -> str:
    """
    Uploads an image to the `up2sha.re`.

    Args:
        client (httpx.AsyncClient): An instance of AsyncClient.
        img (bytes): A byte string representing an image.

    Returns:
        str: The URL of the uploaded image.

    Raises:
        httpx.HTTPStatusError: If the response status code is not successful.
    """
    key = get_env("UP2SHA_KEY")
    ext = get_img_ext(img)
    name = f"img.{ext}"

    response = await client.post(
        url="https://api.up2sha.re/files",
        headers={"X-Api-Key": key},
        files={"file": (name, img)},
    )
    response.raise_for_status()

    return f"{response.json()['public_url'].replace('file?f=', 'media/raw/')}.{ext}"


async def uplio_upload(client: AsyncClient, img: bytes) -> str:
    """
    Uploads an image to the `upl.io`.

    Args:
        client (httpx.AsyncClient): An instance of AsyncClient.
        img (bytes): A byte string representing an image.

    Returns:
        str: The URL of the uploaded image.

    Raises:
        httpx.HTTPStatusError: If the response status code is not successful.
    """
    key = get_env("UPLIO_KEY")
    ext = get_img_ext(img)
    name = f"img.{ext}"

    response = await client.post(
        url="https://upl.io",
        data={"key": key},
        files={"file": (name, img)},
    )
    response.raise_for_status()

    host, uid = response.text.rsplit("/", 1)
    return f"{host}/i/{uid}.{ext}"


async def uploadcare_upload(client: AsyncClient, img: bytes) -> str:
    """
    Uploads an image to the `uploadcare.com`.

    Args:
        client (httpx.AsyncClient): An instance of AsyncClient.
        img (bytes): A byte string representing an image.

    Returns:
        str: The URL of the uploaded image.

    Raises:
        httpx.HTTPStatusError: If the response status code is not successful.
    """
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
    """
    Uploads an image to the `vgy.me`.

    Args:
        client (httpx.AsyncClient): An instance of AsyncClient.
        img (bytes): A byte string representing an image.

    Returns:
        str: The URL of the uploaded image.

    Raises:
        httpx.HTTPStatusError: If the response status code is not successful.
    """
    key = get_env("VGY_KEY")
    name = f"img.{get_img_ext(img)}"

    response = await client.post(
        url="https://vgy.me/upload",
        data={"userkey": key},
        files={"file[]": (name, img)},
    )
    response.raise_for_status()

    return response.json()["image"]


UPLOAD: dict[str, Callable] = {
    "anhmoe": anhmoe_upload,
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
