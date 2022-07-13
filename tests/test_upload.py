#!/usr/bin/env python
from src.py_image_uploader.upload import UPLOAD, geekpic_upload


def test_get_upload_func():
    assert UPLOAD["geekpic"] == geekpic_upload
