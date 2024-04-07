"""Entrypoint for cli."""

import asyncio
import sys
from pathlib import Path

import click
import copykitten
from dotenv import load_dotenv

from images_upload_cli.logger import setup_logger
from images_upload_cli.main import format_link, upload_images
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
@click.option(
    "-f",
    "--format",
    "fmt",
    type=click.Choice(("plain", "bbcode", "html", "markdown")),
    default="plain",
    help="The format of the links to be generated.",
)
@click.option(
    "-t",
    "--thumbnail",
    is_flag=True,
    help="Create captioned thumbnails. By default, in bbcode format.",
)
@click.option(
    "-n",
    "--notify",
    is_flag=True,
    help="Send desktop notification on completion. Required libnotify.",
)
@click.option(
    "--clipboard/--no-clipboard",
    is_flag=True,
    default=True,
    help="Copy the result to the clipboard.",
)
@click.option(
    "--env-file",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="The path to the environment file. Takes precedence over the default config file.",
)
@click.option(
    "--log-level",
    type=click.Choice(("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")),
    default="INFO",
    help="Use DEBUG to show debug logs. Use CRITICAL to suppress all logs.",
)
@click.version_option()
def cli(
    images: tuple[Path],
    hosting: str,
    fmt: str,
    thumbnail: bool,
    notify: bool,
    clipboard: bool,
    env_file: Path,
    log_level: str,
) -> None:
    """Upload images via APIs."""
    """
    Upload images to the specified hosting service, format links, and print.
    Optionally copy links to clipboard and send desktop notification.

    Args:
        images: The paths to the images to upload.
        hosting: The hosting service to use for uploading the images.
        fmt: The format to use for generating the links to the uploaded images.
        thumbnail: Whether thumbnail images should be generated for the uploaded images.
        notify: Whether to send desktop notification on completion.
        clipboard: Whether to copy the image links to the clipboard.
        env_file: The path to the environment file.
        log_level: The log level to use for the logger.
    """
    # Set up logger.
    error_handler = setup_logger(log_level=log_level)
    # Load environment variables.
    load_dotenv(dotenv_path=env_file or get_config_path())

    # Upload images.
    links = asyncio.run(
        upload_images(upload_func=UPLOAD[hosting], images=images, thumbnail=thumbnail)
    )
    # If links are available, format and print them.
    # If thumbnail is enabled and fmt is plain, change fmt to bbcode.
    if links:
        if thumbnail and fmt == "plain":
            fmt = "bbcode"
        formatted_links = format_link(links, fmt)

        click.echo(formatted_links)
        if clipboard:
            copykitten.copy(formatted_links)
        if notify:
            notify_send(formatted_links)

    if error_handler.has_error_occurred():
        sys.exit(1)
