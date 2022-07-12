#!/usr/bin/env python
import pytest

from src.py_image_uploader.upload import (
    geekpic_upload,
    UPLOAD
)


def test_get_upload_func():
    assert UPLOAD("geekpic") == geekpic_upload
