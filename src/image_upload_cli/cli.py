#!/usr/bin/env python
from __future__ import annotations

from pathlib import Path

import click
from dotenv import load_dotenv
from pyperclip import copy

from .upload import HOSTINGS, UPLOAD
from .util import get_config_path, kdialog, make_thumbnail


@click.command(context_settings={"show_default": True})
@click.argument(
    "images", nargs=-1, type=click.Path(exists=True, dir_okay=False, path_type=Path)
)
@click.option("-h", "--hosting", type=click.Choice(HOSTINGS), default="geekpic")
@click.option("-b", "--bbcode", is_flag=True, help="Add bbcode tags.")
@click.option("-t", "--thumbnail", is_flag=True, help="Add thumbnails and bbcode tags.")
@click.option(
    "-c/-C",
    "--clipboard/--no-clipboard",
    is_flag=True,
    default=True,
    help="The result will be copied to the clipboard.",
)
@click.version_option()
def cli(
    images: tuple[Path],
    hosting: str,
    bbcode: bool,
    thumbnail: bool,
    clipboard: bool,
) -> None:
    """
    Upload images via APIs.
    """
    # loading .env variables
    load_dotenv(dotenv_path=get_config_path())

    # get upload func
    upload_func = UPLOAD[hosting]

    # image upload
    links = []
    for img_path in images:
        img = img_path.read_bytes()

        if not thumbnail:
            link = f"[img]{upload_func(img)}[/img]" if bbcode else upload_func(img)
        else:
            thumb = make_thumbnail(img)
            link = f"[url={upload_func(img)}][img]{upload_func(thumb)}[/img][/url]"

        links.append(link)

    # out
    links_str = " ".join(links)
    click.echo(links_str)
    if clipboard:
        copy(links_str)
    kdialog(links_str)


if __name__ == "__main__":
    cli()
