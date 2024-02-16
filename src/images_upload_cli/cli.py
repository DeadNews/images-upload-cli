"""Entrypoint for cli."""

import asyncio
import sys
from collections.abc import Callable
from pathlib import Path

import click
from dotenv import load_dotenv
from httpx import AsyncClient
from pyperclip import copy

from images_upload_cli.image import get_font, make_thumbnail
from images_upload_cli.logger import LOG_LEVELS, setup_logger
from images_upload_cli.upload import HOSTINGS, UPLOAD
from images_upload_cli.util import get_config_path, notify_send


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
    help="Send desktop notification on completion. Required libnotify.",
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
@click.option(
    "--log-level",
    type=click.Choice(LOG_LEVELS),
    default="INFO",
    help="Use DEBUG to show debug logs. Use CRITICAL to suppress all logs.",
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
    log_level: str,
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
        log_level (str): The log level to use for the logger.

    Returns:
        None.
        Prints the links to the uploaded images, optionally copies them to the clipboard, and sends desktop notification.
    """
    # Set up logger
    error_handler = setup_logger(log_level=log_level)
    # Load environment variables
    load_dotenv(dotenv_path=env_file or get_config_path())

    # Upload images
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

    if error_handler.has_error_occurred():
        sys.exit(1)


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
            if thumbnail:
                thumb = make_thumbnail(img, font)  # pyright: ignore[reportPossiblyUnboundVariable]
                thumb_link = await upload_func(client, thumb)
                link = f"[url={img_link}][img]{thumb_link}[/img][/url]"
            else:
                link = f"[img]{img_link}[/img]" if bbcode else img_link

            links.append(link)

    return links
