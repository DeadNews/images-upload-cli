#!/usr/bin/env python
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


@click.command(context_settings={"show_default": True})
@click.argument(
    "images",
    nargs=-1,
    required=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@click.option("-h", "--hosting", type=click.Choice(HOSTINGS), default="imgur")
@click.option("-b", "--bbcode", is_flag=True, help="Add bbcode tags.")
@click.option("-t", "--thumbnail", is_flag=True, help="Add caption thumbnail and bbcode tags.")
@click.option("-n", "--notify", is_flag=True, help="Send desktop notification via libnotify.")
@click.option(
    "-c/-C",
    "--clipboard/--no-clipboard",
    is_flag=True,
    default=True,
    help="Copy result to clipboard.",
)
@click.version_option()
def cli(
    images: tuple[Path],
    hosting: str,
    bbcode: bool,
    thumbnail: bool,
    notify: bool,
    clipboard: bool,
) -> None:
    """
    Upload images via APIs.

    Args:
        images (tuple[Path]): A tuple of `Path` objects representing the paths to the images to be uploaded.
        hosting (str): The hosting service to use for image upload.
        bbcode (bool): A boolean flag indicating whether to generate BBCode links for the uploaded images.
        thumbnail (bool): A boolean flag indicating whether to generate thumbnail images for the uploaded images.
        notify (bool): A boolean flag indicating whether to send desktop notifications.
        clipboard (bool): A boolean flag indicating whether to copy the image links to the clipboard.

    Returns:
        None.
        Prints the links to the uploaded images, optionally copies them to the clipboard and sends desktop notifications.
    """
    load_dotenv(dotenv_path=get_config_path())

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
                thumb_link = await upload_func(client, make_thumbnail(img, font))
                link = f"[url={img_link}][img]{thumb_link}[/img][/url]"

            links.append(link)

    return links
