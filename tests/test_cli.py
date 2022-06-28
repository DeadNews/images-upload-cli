#!/usr/bin/env python
from src.py_image_uploader.cli import parse_args


def test_parse_args_help(capsys):
    parse_args([("-h", "--help")])

    _, err = capsys.readouterr()
    assert err == ""
