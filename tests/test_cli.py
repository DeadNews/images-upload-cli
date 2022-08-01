#!/usr/bin/env python
from click.testing import CliRunner

from src.image_upload_cli.cli import cli


def test_click():
    runner = CliRunner()
    assert runner.invoke(cli, ["--help"]).exit_code == 0


def test_uploadcare():
    runner = CliRunner()
    assert runner.invoke(cli, ["tests/pixel.png", "-h", "uploadcare"]).exit_code == 0
