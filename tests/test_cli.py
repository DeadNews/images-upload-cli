#!/usr/bin/env python
import pytest
from click.testing import CliRunner

from src.image_upload_cli.__main__ import cli


@pytest.mark.parametrize(
    argnames=("args"),
    argvalues=[
        (["--help"]),
        (["tests/test_files/pic.png", "-C", "-h", "imgur"]),
        (["tests/test_files/pic.png", "-C", "-h", "uploadcare", "--thumbnail"]),
    ],
)
def test_help(args: list[str]):
    runner = CliRunner()
    assert runner.invoke(cli=cli, args=args).exit_code == 0
