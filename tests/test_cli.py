#!/usr/bin/env python
import pytest
from click.testing import CliRunner

from src.image_upload_cli.__main__ import cli


@pytest.mark.parametrize(
    argnames=("args"),
    argvalues=[
        (["--help"]),
        (["tests/test_files/pic.png", "-C", "-h", "uploadcare", "--thumbnail"]),
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
        (["tests/test_files/pic.png", "-C", "-h", "catbox"]),
        (["tests/test_files/pic.png", "-C", "-h", "fastpic"]),
        (["tests/test_files/pic.png", "-C", "-h", "filecoffee"]),
        (["tests/test_files/pic.png", "-C", "-h", "freeimage"]),
        (["tests/test_files/pic.png", "-C", "-h", "geekpic"]),
        (["tests/test_files/pic.png", "-C", "-h", "gyazo"]),
        (["tests/test_files/pic.png", "-C", "-h", "imageban"]),
        (["tests/test_files/pic.png", "-C", "-h", "imgbb"]),
        (["tests/test_files/pic.png", "-C", "-h", "imgchest"]),
        (["tests/test_files/pic.png", "-C", "-h", "imgur"]),
        (["tests/test_files/pic.png", "-C", "-h", "pictshare"]),
        (["tests/test_files/pic.png", "-C", "-h", "pixeldrain"]),
        (["tests/test_files/pic.png", "-C", "-h", "pixhost"]),
        (["tests/test_files/pic.png", "-C", "-h", "ptpimg"]),
        (["tests/test_files/pic.png", "-C", "-h", "screenshotting"]),
        (["tests/test_files/pic.png", "-C", "-h", "telegraph"]),
        (["tests/test_files/pic.png", "-C", "-h", "uguu"]),
        (["tests/test_files/pic.png", "-C", "-h", "up2sha"]),
        (["tests/test_files/pic.png", "-C", "-h", "uplio"]),
    ],
)
def test_cli(args: list[str]):
    runner = CliRunner()
    assert runner.invoke(cli=cli, args=args).exit_code == 0
