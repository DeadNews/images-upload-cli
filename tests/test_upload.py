#!/usr/bin/env python
from __future__ import annotations

from src.images_upload_cli.upload import UPLOAD, imgur_upload


def test_get_upload_func():
    assert UPLOAD["imgur"] == imgur_upload
