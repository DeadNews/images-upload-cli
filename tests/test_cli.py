#!/usr/bin/env python
import pytest
from click.testing import CliRunner

from src.image_upload_cli.cli import cli


@pytest.mark.parametrize(
    ("args"),
    [
        (["--help"]),
        (["tests/pic.png", "--no-clipboard", "-h", "geekpic"]),
        (["tests/pic.png", "--no-clipboard", "-h", "uploadcare"]),
    ],
)
def test_cli(args: list[str]):
    runner = CliRunner()
    assert runner.invoke(cli=cli, args=args).exit_code == 0
