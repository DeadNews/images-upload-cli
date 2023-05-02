#!/usr/bin/env python
from __future__ import annotations

import pytest
from click.testing import CliRunner
from images_upload_cli.__main__ import cli
from images_upload_cli.upload import HOSTINGS


@pytest.mark.parametrize(
    argnames=("args"),
    argvalues=[
        pytest.param(["--help"], id="help"),
        pytest.param(
            ["tests/resources/pic.png", "-C", "-h", "uploadcare", "--thumbnail"],
            id="uploadcare,thumbnail",
        ),
    ],
)
def test_cli(args: list[str]):
    runner = CliRunner()
    assert runner.invoke(cli=cli, args=args).exit_code == 0


@pytest.mark.slow()
@pytest.mark.parametrize(
    argnames=("args"),
    argvalues=[
        pytest.param(["tests/resources/pic.png", "-C", "-h", hosting], id=hosting)
        for hosting in HOSTINGS
    ],
)
def test_cli_all(args: list[str]):
    runner = CliRunner()
    assert runner.invoke(cli=cli, args=args).exit_code == 0
