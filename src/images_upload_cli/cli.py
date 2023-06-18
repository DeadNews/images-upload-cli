#!/usr/bin/env python
"""Entrypoint for cli."""
from __future__ import annotations

import asyncio
from collections.abc import Callable  # noqa: TCH003
from pathlib import Path

import click
from aiofiles import open as aopen
from aiohttp import ClientSession
from dotenv import load_dotenv
from pyperclip import copy

from images_upload_cli.upload import HOSTINGS, UPLOAD
from images_upload_cli.util import get_config_path, kdialog, make_thumbnail


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
    clipboard: bool,
) -> None:
    """Upload images via APIs."""
    # loading .env variables
    load_dotenv(dotenv_path=get_config_path())

    # get upload func
    upload_func = UPLOAD[hosting]

    # image upload
    links = asyncio.run(
        upload_image(upload_func, images=images, bbcode=bbcode, thumbnail=thumbnail)
    )

    # out
    links_str = " ".join(links)
    click.echo(links_str)
    if clipboard:
        copy(links_str)
    kdialog(links_str)


async def upload_image(
    upload_func: Callable,
    images: tuple[Path],
    bbcode: bool,
    thumbnail: bool,
) -> list[str]:
    """Upload images."""
    links = []
    async with ClientSession() as session:
        for img_path in images:
            async with aopen(img_path, mode="rb") as f:
                img = await f.read()

                if not thumbnail:
                    img_link = await upload_func(session, img)
                    link = f"[img]{img_link}[/img]" if bbcode else img_link
                else:
                    thumb = make_thumbnail(img)
                    link = f"[url={upload_func(session, img)}][img]{upload_func(session, thumb)}[/img][/url]"

                links.append(link)

    return links
