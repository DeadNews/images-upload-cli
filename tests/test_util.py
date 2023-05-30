#!/usr/bin/env python
from __future__ import annotations

from os import environ
from pathlib import Path

import pytest
from images_upload_cli.util import GetEnvError, get_env, get_img_ext, human_size


@pytest.fixture()
def img() -> bytes:
    return Path("tests/resources/pic.png").read_bytes()


@pytest.mark.parametrize(
    argnames=("test_arg", "expected"),
    argvalues=[
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


def test_get_img_ext(img):
    assert get_img_ext(img) == "png"


def test_get_env():
    environ["TEST_KEY_1"] = "test"
    assert get_env("TEST_KEY_1") == "test"


def test_get_env_error():
    with pytest.raises(GetEnvError):
        get_env("TEST_KEY_2")
