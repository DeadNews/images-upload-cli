"""Entrypoint for cli."""

import asyncio
from collections.abc import Callable
from pathlib import Path

import click
from dotenv import load_dotenv
from httpx import AsyncClient
from pyperclip import copy

from images_upload_cli.upload import HOSTINGS, UPLOAD
from images_upload_cli.util import get_config_path, get_font, make_thumbnail, notify_send


@click.command(context_settings={"max_content_width": 120, "show_default": True})
@click.argument(
    "images",
    nargs=-1,
    required=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@click.option("-h", "--hosting", type=click.Choice(HOSTINGS), default="imgur")
@click.option("-b", "--bbcode", is_flag=True, help="Generate BBCode tags.")
@click.option(
    "-t",
    "--thumbnail",
    is_flag=True,
    help="Create captioned thumbnails. Generate BBCode tags.",
)
@click.option(
    "-n",
    "--notify",
    is_flag=True,
    help="Send desktop notification on completion. Requared libnotify.",
)
@click.option(
    "-c/-C",
    "--clipboard/--no-clipboard",
    is_flag=True,
    default=True,
    show_default=False,
    help="Copy the result to the clipboard. Copies by default.",
)
@click.option(
    "--env-file",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="The path to the environment file. Take precedence over the default config file.",
)
@click.version_option()
def cli(
    images: tuple[Path],
    hosting: str,
    bbcode: bool,
    thumbnail: bool,
    notify: bool,
    clipboard: bool,
    env_file: Path,
) -> None:
    """Upload images via APIs."""
    """
    Args:
        images (tuple[Path]): A tuple of `Path` objects representing the paths to the images to upload.
        hosting (str): The hosting service to use for uploading the images.
        bbcode (bool): A boolean flag indicating whether BBCode tags should be generated for the uploaded images.
        thumbnail (bool): A boolean flag indicating whether thumbnail images should be generated for the uploaded images.
        notify (bool): A boolean flag indicating whether to send desktop notification.
        clipboard (bool): A boolean flag indicating whether to copy the image links to the clipboard.
        env_file (Path): The path to the environment file.

    Returns:
        None.
        Prints the links to the uploaded images, optionally copies them to the clipboard, and sends desktop notification.
    """
    load_dotenv(dotenv_path=env_file or get_config_path())

    links = asyncio.run(
        upload_images(
            upload_func=UPLOAD[hosting],
            images=images,
            bbcode=bbcode,
            thumbnail=thumbnail,
        )
    )

    links_str = " ".join(links)
    click.echo(links_str)
    if clipboard:
        copy(links_str)
    if notify:
        notify_send(links_str)


async def upload_images(
    upload_func: Callable,
    images: tuple[Path],
    bbcode: bool,
    thumbnail: bool,
) -> list[str]:
    """
    Upload images coroutine.

    Args:
        upload_func (Callable): A callable function that handles the actual image upload.
            It takes an `httpx.AsyncClient` instance and the image data as input and returns a link to the uploaded image.
        images (tuple[Path]): A tuple of `Path` objects representing the paths to the images to be uploaded.
        bbcode (bool): A boolean flag indicating whether to generate BBCode links for the uploaded images.
        thumbnail (bool): A boolean flag indicating whether to generate thumbnail images for the uploaded images.

    Returns:
        list[str]: A list of links to the uploaded images. If the `thumbnail` flag is set to True,
            the list includes links to the thumbnail images.
    """
    links = []

    if thumbnail:
        font = get_font()

    async with AsyncClient() as client:
        for img_path in images:
            img = img_path.read_bytes()

            img_link = await upload_func(client, img)
            if not thumbnail:
                link = f"[img]{img_link}[/img]" if bbcode else img_link
            else:
                thumb = make_thumbnail(img, font)  # pyright: ignore[reportPossiblyUnboundVariable]
                thumb_link = await upload_func(client, thumb)
                link = f"[url={img_link}][img]{thumb_link}[/img][/url]"

            links.append(link)

    return links
