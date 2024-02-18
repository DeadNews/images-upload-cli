"""Main logic for the images-upload-cli package."""

from collections.abc import Callable
from pathlib import Path

from httpx import AsyncClient

from images_upload_cli.image import get_font, make_thumbnail


async def upload_images(
    upload_func: Callable,
    images: tuple[Path],
    thumbnail: bool,
) -> list[tuple[str, str | None]]:
    """
    Uploads images using the specified upload function.

    Args:
        upload_func (Callable): The function used to upload the images.
        images (tuple[Path]): The paths of the images to be uploaded.
        thumbnail (bool): Indicates whether to generate thumbnails for the images.

    Returns:
        list[tuple[str, str | None]]: A list of tuples containing the links to the uploaded images
            and their corresponding thumbnails (if generated). The thumbnail link will be None if
            thumbnails are not generated.
    """
    links = []

    if thumbnail:
        font = get_font()

    async with AsyncClient() as client:
        for img_path in images:
            img = img_path.read_bytes()

            img_link = await upload_func(client, img=img)
            # If the upload fails, skip the current image and proceed with the next one.
            if not img_link:
                continue

            if thumbnail:
                thumb = make_thumbnail(img, font)  # pyright: ignore[reportPossiblyUnboundVariable]
                thumb_link = await upload_func(client, img=thumb)
                # If the upload fails, skip the current image and proceed with the next one.
                if not thumb_link:
                    continue
            else:
                thumb_link = None

            links.append((img_link, thumb_link))

    return links


def format_link(links: list[tuple[str, str | None]], link_fmt: str) -> str:
    """
    Format the image links based on the specified format.

    Args:
        links (list[tuple[str, str | None]]): A list of tuples containing image links and optional thumbnail links.
        link_fmt (str): The desired format for the image links. Valid options are "plain", "bbcode", "html", and "markdown".

    Returns:
        str: The formatted image links.
    """
    if link_fmt == "plain":
        return " ".join([img_link for img_link, _ in links])

    if link_fmt == "bbcode":
        return " ".join(
            f"[url]{img_link}[/url]"
            if thumb_link is None
            else f"[url={img_link}][img]{thumb_link}[/img][/url]"
            for img_link, thumb_link in links
        )

    if link_fmt == "html":
        return " ".join(
            f'<img src="{img_link}" alt="image">'
            if thumb_link is None
            else f'<a href="{img_link}"><img src="{thumb_link}" alt="thumb"></a>'
            for img_link, thumb_link in links
        )

    if link_fmt == "markdown":
        return " ".join(
            f"![image]({img_link})"
            if thumb_link is None
            else f"[![thumb]({thumb_link})]({img_link})"
            for img_link, thumb_link in links
        )

    return ""
