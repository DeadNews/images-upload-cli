#!/usr/bin/env python
from src.image_upload_cli.upload import UPLOAD, imgur_upload


def test_get_upload_func():
    assert UPLOAD["imgur"] == imgur_upload
