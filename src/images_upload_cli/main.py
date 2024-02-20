"""Main logic for the images-upload-cli package."""

from collections.abc import Awaitable, Callable, Sequence
from pathlib import Path

from httpx import AsyncClient

from images_upload_cli.image import get_font, make_thumbnail


async def upload_images(
    upload_func: Callable[[AsyncClient, bytes], Awaitable[str]],
    images: tuple[Path],
    thumbnail: bool,
) -> Sequence[tuple[str, str] | tuple[str, None]]:
    """Upload images using the specified upload function and optionally generate thumbnails.

    Args:
        upload_func: The function used to upload the images.
        images: The paths of the images to be uploaded.
        thumbnail: Indicates whether to generate thumbnails for the images.

    Returns:
        The links to the uploaded images and their corresponding thumbnails.
        The thumbnail link will be `None` if generation is disabled.
    """
    links = []
    font = get_font() if thumbnail else None

    async with AsyncClient() as client:
        for img_path in images:
            img = img_path.read_bytes()

            img_link = await upload_func(client, img)
            # If the upload fails, skip the current image and proceed with the next one.
            if not img_link:
                continue

            if thumbnail:
                thumb = make_thumbnail(img, font=get_font() if font is None else font)
                thumb_link = await upload_func(client, thumb)
                # If the upload fails, skip the current image and proceed with the next one.
                if not thumb_link:
                    continue
            else:
                thumb_link = None

            links.append((img_link, thumb_link))

    return links


def format_link(links: Sequence[tuple[str, str] | tuple[str, None]], fmt: str) -> str:
    """Format the image links based on the specified format.

    Args:
        links: The image links and optional thumbnail links.
        fmt: The format to use for formatting the links. Valid options are "plain", "bbcode", "html", and "markdown".

    Returns:
        The formatted image links as a string.
    """
    if fmt == "plain":
        return " ".join([img_link for img_link, _ in links])

    if fmt == "bbcode":
        return " ".join(
            f"[img]{img_link}[/img]"
            if thumb_link is None
            else f"[url={img_link}][img]{thumb_link}[/img][/url]"
            for img_link, thumb_link in links
        )

    if fmt == "html":
        return " ".join(
            f'<img src="{img_link}" alt="image">'
            if thumb_link is None
            else f'<a href="{img_link}"><img src="{thumb_link}" alt="thumb"></a>'
            for img_link, thumb_link in links
        )

    if fmt == "markdown":
        return " ".join(
            f"![image]({img_link})"
            if thumb_link is None
            else f"[![thumb]({thumb_link})]({img_link})"
            for img_link, thumb_link in links
        )

    return ""
