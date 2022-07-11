#!/usr/bin/env python
"""
Upload images via APIs
"""
from __future__ import annotations

from argparse import ArgumentParser, Namespace
from collections.abc import Sequence
from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from pyperclip import copy as copy_to_clipboard

from .__version__ import __version__
from .upload import get_upload_func
from .util import kdialog, make_thumbnail


def parse_args(args: Sequence[str] | None = None) -> Namespace:
    parser = ArgumentParser(description=__doc__)

    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        dest="input_files",
        type=str,
        nargs="+",
        help="Path to the input files",
    )
    parser.add_argument(
        "-s",
        "--server_name",
        type=str.lower,
        choices={
            "fastpic",
            "freeimage",
            "geekpic",
            "imageban",
            "imageshack",
            "imgbb",
            "imgur",
            "pixhost",
            "uploadcare",
        },
        default="geekpic",
        help="Hosting for uploading images",
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-b",
        "--bbcode",
        action="store_true",
        default=False,
        help="Add bbcode tags",
    )
    group.add_argument(
        "-t",
        "--thumbnail",
        action="store_true",
        default=False,
        help="Generate thumbnails",
    )

    return parser.parse_args(args)


def main() -> None:
    """
    Upload images via APIs
    """
    args = parse_args()

    # loading .env variables
    load_dotenv(dotenv_path=find_dotenv())

    # get upload func
    upload_func = get_upload_func(server_name=args.server_name)

    # image uploader
    links = []
    for f1 in args.input_files:
        img_path = Path(f1)
        img = img_path.read_bytes()

        if not args.thumbnail:
            link = f"[img]{upload_func(img)}[/img]" if args.bbcode else upload_func(img)
        else:
            thumbnail = make_thumbnail(img_path)
            link = f"[url={upload_func(img)}][img]{upload_func(thumbnail)}[/img][/url]"

        links.append(link)

    # out
    links_str = " ".join(links)
    print(links_str)
    copy_to_clipboard(links_str)
    kdialog(links_str)


if __name__ == "__main__":
    main()
