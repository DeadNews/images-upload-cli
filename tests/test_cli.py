#!/usr/bin/env python
from shutil import which

import pytest
from click.testing import CliRunner

from src.image_upload_cli.cli import cli


@pytest.mark.parametrize(
    ("args"),
    [
        (["--help"]),
        (["tests/pic.png", "-h", "geekpic"]),
        (["tests/pic.png", "-h", "uploadcare"]),
    ],
)
def test_cli(args: list[str]):
    runner = CliRunner()
    assert runner.invoke(cli=cli, args=args).exit_code == 0


def test_xclip():
    assert which("xclip") is not None
