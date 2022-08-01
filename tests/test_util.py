#!/usr/bin/env python
from os import environ

import pytest

from src.image_upload_cli.util import GetenvError, get_env_val, get_img_ext, human_size


@pytest.mark.parametrize(
    ("test_arg", "expected"),
    [
        (1, "1.0 B"),
        (300, "300.0 B"),
        (3000, "2.9 KiB"),
        (3000000, "2.9 MiB"),
        (1024, "1.0 KiB"),
        (10**26 * 30, "2481.5 YiB"),
    ],
)
def test_human_size(test_arg: int, expected: str):
    assert human_size(test_arg) == expected

    args_with_negative = test_arg * -1
    assert human_size(args_with_negative) == f"-{expected}"


def test_get_img_ext():
    img = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x01sRGB\x00\xae\xce\x1c\xe9\x00\x00\x00\x04gAMA\x00\x00\xb1\x8f\x0b\xfca\x05\x00\x00\x00\tpHYs\x00\x00\x0e\xc3\x00\x00\x0e\xc3\x01\xc7o\xa8d\x00\x00\x00\rIDAT\x18Wc`dd\xfc\x0f\x00\x01\r\x01\x03\xcb\x11t\xdb\x00\x00\x00\x00IEND\xaeB`\x82"

    assert get_img_ext(img) == "png"


def test_get_env_val():
    environ["TEST_KEY_1"] = "test"
    assert get_env_val("TEST_KEY_1") == "test"


def test_get_env_val_error():
    with pytest.raises(GetenvError):
        get_env_val("TEST_KEY_2")
