#!/usr/bin/env python
import pytest
from click.testing import CliRunner

from src.images_upload_cli.__main__ import cli


@pytest.mark.parametrize(
    argnames=("args"),
    argvalues=[
        (["--help"]),
        (["tests/resources/pic.png", "-C", "-h", "uploadcare", "--thumbnail"]),
    ],
)
def test_cli_fast(args: list[str]):
    runner = CliRunner()
    assert runner.invoke(cli=cli, args=args).exit_code == 0


@pytest.mark.slow()
@pytest.mark.parametrize(
    argnames=("args"),
    argvalues=[
        (["--help"]),
        (["tests/resources/pic.png", "-C", "-h", "catbox"]),
        (["tests/resources/pic.png", "-C", "-h", "fastpic"]),
        (["tests/resources/pic.png", "-C", "-h", "filecoffee"]),
        (["tests/resources/pic.png", "-C", "-h", "freeimage"]),
        (["tests/resources/pic.png", "-C", "-h", "geekpic"]),
        (["tests/resources/pic.png", "-C", "-h", "gyazo"]),
        (["tests/resources/pic.png", "-C", "-h", "imageban"]),
        (["tests/resources/pic.png", "-C", "-h", "imgbb"]),
        (["tests/resources/pic.png", "-C", "-h", "imgchest"]),
        (["tests/resources/pic.png", "-C", "-h", "imgur"]),
        (["tests/resources/pic.png", "-C", "-h", "pictshare"]),
        (["tests/resources/pic.png", "-C", "-h", "pixeldrain"]),
        (["tests/resources/pic.png", "-C", "-h", "pixhost"]),
        (["tests/resources/pic.png", "-C", "-h", "ptpimg"]),
        (["tests/resources/pic.png", "-C", "-h", "screenshotting"]),
        (["tests/resources/pic.png", "-C", "-h", "smms"]),
        (["tests/resources/pic.png", "-C", "-h", "sxcu"]),
        (["tests/resources/pic.png", "-C", "-h", "telegraph"]),
        (["tests/resources/pic.png", "-C", "-h", "up2sha"]),
        (["tests/resources/pic.png", "-C", "-h", "uplio"]),
    ],
)
def test_cli(args: list[str]):
    runner = CliRunner()
    assert runner.invoke(cli=cli, args=args).exit_code == 0
