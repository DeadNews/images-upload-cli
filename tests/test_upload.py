#!/usr/bin/env python
from src.image_upload_cli.upload import UPLOAD, geekpic_upload


def test_get_upload_func():
    assert UPLOAD["geekpic"] == geekpic_upload
