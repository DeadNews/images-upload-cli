#!/usr/bin/env python
from click.testing import CliRunner

from src.py_image_uploader.cli import main


def test_click():
    runner = CliRunner()
    assert runner.invoke(cli=main, args=["--help"]).exit_code == 0
    assert runner.invoke(cli=main, args=["--bbcode"]).exit_code == 0
