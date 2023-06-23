#!/usr/bin/env python
"""Entrypoint for cli."""

import asyncio
from collections.abc import Callable
from pathlib import Path
from typing import Annotated

import click
import typer
from dotenv import load_dotenv
from httpx import AsyncClient
from pyperclip import copy

from images_upload_cli.upload import HOSTINGS, UPLOAD
from images_upload_cli.util import get_config_path, make_thumbnail, notify_send

app = typer.Typer()


@app.command()
def cli(
    images: Annotated[list[Path], typer.Argument(exists=True, dir_okay=False)],
    hosting: Annotated[
        str, typer.Option("-h", "--hosting", click_type=click.Choice(HOSTINGS))
    ] = "imgur",
    bbcode: Annotated[bool, typer.Option("-b", "--bbcode", help="Add bbcode tags.")] = False,
    thumbnail: Annotated[
        bool, typer.Option("-t", "--thumbnail", help="Add caption thumbnail and bbcode tags.")
    ] = False,
    notify: Annotated[
        bool, typer.Option("-n", "--notify", help="Send desktop notifications via libnotify.")
    ] = False,
    clipboard: Annotated[
        bool, typer.Option("-c/-C", "--clipboard/--no-clipboard", help="Copy result to clipboard.")
    ] = True,
) -> None:
    """Upload images via APIs."""
    # loading .env variables
    load_dotenv(dotenv_path=get_config_path())

    # async images upload
    links = asyncio.run(
        upload_images(
            upload_func=UPLOAD[hosting],
            images=images,
            bbcode=bbcode,
            thumbnail=thumbnail,
        )
    )

    # out
    links_str = " ".join(links)
    click.echo(links_str)
    if clipboard:
        copy(links_str)
    if notify:
        notify_send(links_str)


async def upload_images(
    upload_func: Callable,
    images: list[Path],
    bbcode: bool,
    thumbnail: bool,
) -> list[str]:
    """Upload images coroutine."""
    links = []

    async with AsyncClient() as client:
        for img_path in images:
            img = img_path.read_bytes()

            img_link = await upload_func(client, img)
            if not thumbnail:
                link = f"[img]{img_link}[/img]" if bbcode else img_link
            else:
                thumb_link = await upload_func(client, make_thumbnail(img))
                link = f"[url={img_link}][img]{thumb_link}[/img][/url]"

            links.append(link)

    return links
