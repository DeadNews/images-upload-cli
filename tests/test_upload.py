#!/usr/bin/env python
import pytest

from src.py_image_uploader.upload import (
    InvalidParameterError,
    geekpic_upload,
    get_upload_func,
)


def test_get_upload_func() -> None:
    assert get_upload_func("geekpic") == geekpic_upload


def test_get_upload_func_err() -> None:
    with pytest.raises(InvalidParameterError):
        get_upload_func("random_value")
