#!/usr/bin/env python
"""
Upload images via APIs
"""
from __future__ import annotations

from pathlib import Path

import click
from dotenv import find_dotenv, load_dotenv
from pyperclip import copy as copy_to_clipboard

from .upload import HOSTINGS_LIST, get_upload_func
from .util import kdialog, make_thumbnail


@click.command(context_settings={"show_default": True})
@click.argument("images", nargs=-1, type=Path)
@click.option("-h", "--hosting", type=click.Choice(HOSTINGS_LIST), default="geekpic")
@click.option("-b", "--bbcode", is_flag=True, help="Add bbcode tags")
@click.option("-t", "--thumbnail", is_flag=True, help="Add thumbnails and bbcode tags")
@click.version_option()
def main(images: list[Path], hosting: str, bbcode: bool, thumbnail: bool) -> None:
    """
    Upload images via APIs
    """
    # loading .env variables
    load_dotenv(dotenv_path=find_dotenv())

    # get upload func
    upload_func = get_upload_func(server_name=hosting)

    # image uploader
    links = []
    for img_path in images:
        img = img_path.read_bytes()

        if not thumbnail:
            link = f"[img]{upload_func(img)}[/img]" if bbcode else upload_func(img)
        else:
            thmb = make_thumbnail(img_path)
            link = f"[url={upload_func(img)}][img]{upload_func(thmb)}[/img][/url]"

        links.append(link)

    # out
    links_str = " ".join(links)
    click.echo(links_str)
    copy_to_clipboard(links_str)
    kdialog(links_str)


if __name__ == "__main__":
    main(main)
