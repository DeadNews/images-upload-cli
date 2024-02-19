"""Upload images to various hosting services."""

from collections.abc import Callable
from os import getenv
from re import search
from urllib.parse import urlparse

from httpx import AsyncClient
from loguru import logger

from images_upload_cli.image import get_img_ext
from images_upload_cli.util import get_env, log_on_error


@logger.catch(default="")
async def anhmoe_upload(client: AsyncClient, img: bytes) -> str:
    """
    Uploads an image to the `anh.mo`.

    Args:
        client (httpx.AsyncClient): The async HTTP client used to make the API request.
        img (bytes): The image data to be uploaded.

    Returns:
        str: The URL of the uploaded image, or an empty string if the upload failed.
    """
    key = "anh.moe_public_api"

    response = await client.post(
        url="https://anh.moe/api/1/upload",
        data={"key": key},
        files={"source": img},
    )
    if response.is_error:
        log_on_error(response)
        return ""

    return response.json()["image"]["url"]


@logger.catch(default="")
async def beeimg_upload(client: AsyncClient, img: bytes) -> str:
    """
    Uploads an image to the `beeimg.com`.

    Args:
        client (httpx.AsyncClient): The async HTTP client used to make the API request.
        img (bytes): The image data to be uploaded.

    Returns:
        str: The URL of the uploaded image, or an empty string if the upload failed.
    """
    ext = get_img_ext(img)
    name = f"img.{ext}"
    content_type = f"image/{ext}"

    response = await client.post(
        url="https://beeimg.com/api/upload/file/json/",
        files={"file": (name, img, content_type)},
    )
    if response.is_error:
        log_on_error(response)
        return ""

    return f"https:{response.json()['files']['url']}"


@logger.catch(default="")
async def catbox_upload(client: AsyncClient, img: bytes) -> str:
    """
    Uploads an image to the `catbox.moe`.

    Args:
        client (httpx.AsyncClient): The async HTTP client used to make the API request.
        img (bytes): The image data to be uploaded.

    Returns:
        str: The URL of the uploaded image, or an empty string if the upload failed.
    """
    response = await client.post(
        url="https://catbox.moe/user/api.php",
        data={"reqtype": "fileupload"},
        files={"fileToUpload": img},
    )
    if response.is_error:
        log_on_error(response)
        return ""

    return response.text


@logger.catch(default="")
async def fastpic_upload(client: AsyncClient, img: bytes) -> str:
    """
    Uploads an image to the `fastpic.org`.

    Args:
        client (httpx.AsyncClient): The async HTTP client used to make the API request.
        img (bytes): The image data to be uploaded.

    Returns:
        str: The URL of the uploaded image, or an empty string if the upload failed.
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
    if response.is_error:
        log_on_error(response)
        return ""

    match = search(r"<imagepath>(.+?)</imagepath>", response.text)
    if match is None:
        logger.error(f"Image link not found in '{response.url}' response.")
        logger.debug(f"Response text:\n{response.text}")
        return ""

    return match[1].strip()


@logger.catch(default="")
async def filecoffee_upload(client: AsyncClient, img: bytes) -> str:
    """
    Uploads an image to the `file.coffee`.

    Args:
        client (httpx.AsyncClient): The async HTTP client used to make the API request.
        img (bytes): The image data to be uploaded.

    Returns:
        str: The URL of the uploaded image, or an empty string if the upload failed.
    """
    response = await client.post(
        url="https://file.coffee/api/file/upload",
        files={"file": img},
    )
    if response.is_error:
        log_on_error(response)
        return ""

    return response.json()["url"]


@logger.catch(default="")
async def freeimage_upload(client: AsyncClient, img: bytes) -> str:
    """
    Uploads an image to the `freeimage.host`.

    Args:
        client (httpx.AsyncClient): The async HTTP client used to make the API request.
        img (bytes): The image data to be uploaded.

    Returns:
        str: The URL of the uploaded image, or an empty string if the upload failed.
    """
    key = get_env("FREEIMAGE_KEY")

    response = await client.post(
        url="https://freeimage.host/api/1/upload",
        data={"key": key},
        files={"source": img},
    )
    if response.is_error:
        log_on_error(response)
        return ""

    return response.json()["image"]["url"]


@logger.catch(default="")
async def gyazo_upload(client: AsyncClient, img: bytes) -> str:
    """
    Uploads an image to the `gyazo.com`.

    Args:
        client (httpx.AsyncClient): The async HTTP client used to make the API request.
        img (bytes): The image data to be uploaded.

    Returns:
        str: The URL of the uploaded image, or an empty string if the upload failed.
    """
    key = get_env("GYAZO_TOKEN")

    response = await client.post(
        url=f"https://upload.gyazo.com/api/upload?access_token={key}",
        files={"imagedata": img},
    )
    if response.is_error:
        log_on_error(response)
        return ""

    return response.json()["url"]


@logger.catch(default="")
async def imageban_upload(client: AsyncClient, img: bytes) -> str:
    """
    Uploads an image to the `imageban.ru`.

    Args:
        client (httpx.AsyncClient): The async HTTP client used to make the API request.
        img (bytes): The image data to be uploaded.

    Returns:
        str: The URL of the uploaded image, or an empty string if the upload failed.
    """
    token = get_env("IMAGEBAN_TOKEN")

    response = await client.post(
        url="https://api.imageban.ru/v1",
        headers={"Authorization": f"TOKEN {token}"},
        files={"image": img},
    )
    if response.is_error:
        log_on_error(response)
        return ""

    return response.json()["data"]["link"]


@logger.catch(default="")
async def imagebin_upload(client: AsyncClient, img: bytes) -> str:
    """
    Uploads an image to the `imagebin.ca`.

    Args:
        client (httpx.AsyncClient): The async HTTP client used to make the API request.
        img (bytes): The image data to be uploaded.

    Returns:
        str: The URL of the uploaded image, or an empty string if the upload failed.
    """
    response = await client.post(
        url="https://imagebin.ca/upload.php",
        files={"file": img},
    )
    if response.is_error:
        log_on_error(response)
        return ""

    match = search(r"url:(.+?)$", response.text)
    if match is None:
        logger.error(f"Image link not found in '{response.url}' response.")
        logger.debug(f"Response text:\n{response.text}")
        return ""

    return match[1].strip()


@logger.catch(default="")
async def imgbb_upload(client: AsyncClient, img: bytes) -> str:
    """
    Uploads an image to the `imgbb.com`.

    Args:
        client (httpx.AsyncClient): The async HTTP client used to make the API request.
        img (bytes): The image data to be uploaded.

    Returns:
        str: The URL of the uploaded image, or an empty string if the upload failed.
    """
    key = get_env("IMGBB_KEY")

    response = await client.post(
        url="https://api.imgbb.com/1/upload",
        data={"key": key},
        files={"image": img},
    )
    if response.is_error:
        log_on_error(response)
        return ""

    return response.json()["data"]["url"]


@logger.catch(default="")
async def imgchest_upload(client: AsyncClient, img: bytes) -> str:
    """
    Uploads an image to the `imgchest.com`.

    Args:
        client (httpx.AsyncClient): The async HTTP client used to make the API request.
        img (bytes): The image data to be uploaded.

    Returns:
        str: The URL of the uploaded image, or an empty string if the upload failed.
    """
    key = get_env("IMGCHEST_KEY")
    name = f"img.{get_img_ext(img)}"

    response = await client.post(
        url="https://api.imgchest.com/v1/post",
        headers={"Authorization": f"Bearer {key}"},
        files={"images[]": (name, img)},
    )
    if response.is_error:
        log_on_error(response)
        return ""

    return response.json()["data"]["images"][0]["link"]


@logger.catch(default="")
async def imgur_upload(client: AsyncClient, img: bytes) -> str:
    """
    Uploads an image to the `imgur.com`.

    Args:
        client (httpx.AsyncClient): The async HTTP client used to make the API request.
        img (bytes): The image data to be uploaded.

    Returns:
        str: The URL of the uploaded image, or an empty string if the upload failed.
    """
    client_id = getenv("IMGUR_CLIENT_ID", "dd32dd3c6aaa9a0")

    response = await client.post(
        url="https://api.imgur.com/3/image",
        headers={"Authorization": f"Client-ID {client_id}"},
        files={"image": img},
    )
    if response.is_error:
        log_on_error(response)
        return ""

    return response.json()["data"]["link"]


@logger.catch(default="")
async def lensdump_upload(client: AsyncClient, img: bytes) -> str:
    """
    Uploads an image to the `lensdump.com`.

    Args:
        client (httpx.AsyncClient): The async HTTP client used to make the API request.
        img (bytes): The image data to be uploaded.

    Returns:
        str: The URL of the uploaded image, or an empty string if the upload failed.
    """
    key = get_env("LENSDUMP_KEY")

    response = await client.post(
        url="https://lensdump.com/api/1/upload",
        data={"key": key},
        files={"source": img},
    )
    if response.is_error:
        log_on_error(response)
        return ""

    return response.json()["image"]["url"]


@logger.catch(default="")
async def pixeldrain_upload(client: AsyncClient, img: bytes) -> str:
    """
    Uploads an image to the `pixeldrain.com`.

    Args:
        client (httpx.AsyncClient): The async HTTP client used to make the API request.
        img (bytes): The image data to be uploaded.

    Returns:
        str: The URL of the uploaded image, or an empty string if the upload failed.
    """
    response = await client.post(
        url="https://pixeldrain.com/api/file",
        files={"file": img},
    )
    if response.is_error:
        log_on_error(response)
        return ""

    return f"https://pixeldrain.com/api/file/{response.json()['id']}"


@logger.catch(default="")
async def pixhost_upload(client: AsyncClient, img: bytes) -> str:
    """
    Uploads an image to the `pixhost.to`.

    Args:
        client (httpx.AsyncClient): The async HTTP client used to make the API request.
        img (bytes): The image data to be uploaded.

    Returns:
        str: The URL of the uploaded image, or an empty string if the upload failed.
    """
    response = await client.post(
        url="https://api.pixhost.to/images",
        data={"content_type": 0},
        files={"img": img},
    )
    if response.is_error:
        log_on_error(response)
        return ""

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


@logger.catch(default="")
async def ptpimg_upload(client: AsyncClient, img: bytes) -> str:
    """
    Uploads an image to the `ptpimg.me`.

    Args:
        client (httpx.AsyncClient): The async HTTP client used to make the API request.
        img (bytes): The image data to be uploaded.

    Returns:
        str: The URL of the uploaded image, or an empty string if the upload failed.
    """
    key = get_env("PTPIMG_KEY")

    response = await client.post(
        url="https://ptpimg.me/upload.php",
        data={"api_key": key},
        files={"file-upload[0]": img},
    )
    if response.is_error:
        log_on_error(response)
        return ""

    return f"https://ptpimg.me/{response.json()[0]['code']}.{response.json()[0]['ext']}"


@logger.catch(default="")
async def smms_upload(client: AsyncClient, img: bytes) -> str:
    """
    Uploads an image to the `sm.ms`.

    Args:
        client (httpx.AsyncClient): The async HTTP client used to make the API request.
        img (bytes): The image data to be uploaded.

    Returns:
        str: The URL of the uploaded image, or an empty string if the upload failed.
    """
    key = get_env("SMMS_KEY")

    response = await client.post(
        url="https://sm.ms/api/v2/upload",
        headers={"Authorization": key},
        files={"smfile": img},
    )
    if response.is_error:
        log_on_error(response)
        return ""

    json = response.json()

    return json["images"] if json["code"] == "image_repeated" else json["data"]["url"]


@logger.catch(default="")
async def sxcu_upload(client: AsyncClient, img: bytes) -> str:
    """
    Uploads an image to the `sxcu.net`.

    Args:
        client (httpx.AsyncClient): The async HTTP client used to make the API request.
        img (bytes): The image data to be uploaded.

    Returns:
        str: The URL of the uploaded image, or an empty string if the upload failed.
    """
    response = await client.post(
        url="https://sxcu.net/api/files/create",
        headers={"user-agent": "python-https/1.0.0"},
        files={"file": img},
    )
    if response.is_error:
        log_on_error(response)
        return ""

    return f"{response.json()['url']}.{get_img_ext(img)}"


@logger.catch(default="")
async def telegraph_upload(client: AsyncClient, img: bytes) -> str:
    """
    Uploads an image to the `telegra.ph`.

    Args:
        client (httpx.AsyncClient): The async HTTP client used to make the API request.
        img (bytes): The image data to be uploaded.

    Returns:
        str: The URL of the uploaded image, or an empty string if the upload failed.
    """
    response = await client.post(
        url="https://telegra.ph/upload",
        files={"file": img},
    )
    if response.is_error:
        log_on_error(response)
        return ""

    return f"https://telegra.ph{response.json()[0]['src']}"


@logger.catch(default="")
async def thumbsnap_upload(client: AsyncClient, img: bytes) -> str:
    """
    Uploads an image to the `thumbsnap.com`.

    Args:
        client (httpx.AsyncClient): The async HTTP client used to make the API request.
        img (bytes): The image data to be uploaded.

    Returns:
        str: The URL of the uploaded image, or an empty string if the upload failed.
    """
    key = get_env("THUMBSNAP_KEY")

    response = await client.post(
        url="https://thumbsnap.com/api/upload",
        data={"key": key},
        files={"media": img},
    )
    if response.is_error:
        log_on_error(response)
        return ""

    return response.json()["data"]["media"]


@logger.catch(default="")
async def tixte_upload(client: AsyncClient, img: bytes) -> str:
    """Upload to tixte.com."""
    """
    Uploads an image to the `freeimage.host`.

    Args:
        client (httpx.AsyncClient): The async HTTP client used to make the API request.
        img (bytes): The image data to be uploaded.

    Returns:
        str: The URL of the uploaded image, or an empty string if the upload failed.
    """
    key = get_env("TIXTE_KEY")
    name = f"img.{get_img_ext(img)}"

    response = await client.post(
        url="https://api.tixte.com/v1/upload",
        headers={"Authorization": key},
        data={"payload_json": '{"random":true}'},
        files={"file": (name, img)},
    )
    if response.is_error:
        log_on_error(response)
        return ""

    return response.json()["data"]["direct_url"]


@logger.catch(default="")
async def up2sha_upload(client: AsyncClient, img: bytes) -> str:
    """
    Uploads an image to the `up2sha.re`.

    Args:
        client (httpx.AsyncClient): The async HTTP client used to make the API request.
        img (bytes): The image data to be uploaded.

    Returns:
        str: The URL of the uploaded image, or an empty string if the upload failed.
    """
    key = get_env("UP2SHA_KEY")
    ext = get_img_ext(img)
    name = f"img.{ext}"

    response = await client.post(
        url="https://api.up2sha.re/files",
        headers={"X-Api-Key": key},
        files={"file": (name, img)},
    )
    if response.is_error:
        log_on_error(response)
        return ""

    return f"{response.json()['public_url'].replace('file?f=', 'media/raw/')}.{ext}"


@logger.catch(default="")
async def uplio_upload(client: AsyncClient, img: bytes) -> str:
    """
    Uploads an image to the `upl.io`.

    Args:
        client (httpx.AsyncClient): The async HTTP client used to make the API request.
        img (bytes): The image data to be uploaded.

    Returns:
        str: The URL of the uploaded image, or an empty string if the upload failed.
    """
    key = get_env("UPLIO_KEY")
    ext = get_img_ext(img)
    name = f"img.{ext}"

    response = await client.post(
        url="https://upl.io",
        data={"key": key},
        files={"file": (name, img)},
    )
    if response.is_error:
        log_on_error(response)
        return ""

    host, uid = response.text.rsplit("/", 1)
    return f"{host}/i/{uid}.{ext}"


@logger.catch(default="")
async def uploadcare_upload(client: AsyncClient, img: bytes) -> str:
    """
    Uploads an image to the `uploadcare.com`.

    Args:
        client (httpx.AsyncClient): The async HTTP client used to make the API request.
        img (bytes): The image data to be uploaded.

    Returns:
        str: The URL of the uploaded image, or an empty string if the upload failed.
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
    if response.is_error:
        log_on_error(response)
        return ""

    return f"https://ucarecdn.com/{response.json()['filename']}/{name}"


@logger.catch(default="")
async def vgy_upload(client: AsyncClient, img: bytes) -> str:
    """
    Uploads an image to the `vgy.me`.

    Args:
        client (httpx.AsyncClient): The async HTTP client used to make the API request.
        img (bytes): The image data to be uploaded.

    Returns:
        str: The URL of the uploaded image, or an empty string if the upload failed.
    """
    key = get_env("VGY_KEY")
    name = f"img.{get_img_ext(img)}"

    response = await client.post(
        url="https://vgy.me/upload",
        data={"userkey": key},
        files={"file[]": (name, img)},
    )
    if response.is_error:
        log_on_error(response)
        return ""

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
