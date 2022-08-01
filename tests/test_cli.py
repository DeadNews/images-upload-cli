#!/usr/bin/env python
from click.testing import CliRunner

from src.py_image_uploader.cli import cli


def test_click():
    runner = CliRunner()
    assert runner.invoke(cli=cli, args=["--help"]).exit_code == 0
