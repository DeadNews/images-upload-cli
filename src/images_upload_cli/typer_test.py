#!/usr/bin/env python
"""Upload images via APIs."""
from enum import Enum
from pathlib import Path
from typing import Annotated

import typer


class Hostings(Enum):
    """Hostings."""

    fastpic = "fastpic"
    imgur = "imgur"


def main(
    images: Annotated[
        list[Path],
        typer.Argument(
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
        ),
    ],
    hosting: Annotated[Hostings, typer.Option(case_sensitive=False)] = Hostings.imgur,
    bbcode: Annotated[bool, typer.Option("-b", "--bbcode", help="Add bbcode tags.")] = False,
    thumbnail: Annotated[
        bool,
        typer.Option("-t", "--thumbnail", help="Add caption thumbnail and bbcode tags."),
    ] = False,
    notify: Annotated[
        bool,
        typer.Option("-n", "--notify", help="Send desktop notifications via libnotify."),
    ] = False,
    clipboard: Annotated[
        bool,
        typer.Option("-c/-C", "--clipboard/--no-clipboard", help="Copy result to clipboard."),
    ] = True,
) -> None:
    """Upload images via APIs."""
    typer.echo(f"{images=}")
    typer.echo(f"{hosting=}")
    typer.echo(f"{hosting.value=}")
    typer.echo(f"{bbcode=}")
    typer.echo(f"{thumbnail=}")
    typer.echo(f"{notify=}")
    typer.echo(f"{clipboard=}")


if __name__ == "__main__":
    typer.run(main)
