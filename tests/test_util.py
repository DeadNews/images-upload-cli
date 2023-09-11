#!/usr/bin/env python
from os import environ

import pytest
from images_upload_cli.util import GetEnvError, get_env, get_font, get_img_ext, human_size
from PIL import ImageFont


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
def test_human_size(test_arg: int, expected: str) -> None:
    """
    Test the human_size function.

    Args:
        test_arg (int): The number of bytes to be converted.
        expected (str): The expected human-readable size with the appropriate unit and suffix.

    Raises:
        AssertionError: If the output of calling human_size with test_arg is not equal to expected.
                        If the output of calling human_size with the negation of test_arg is not equal to the negation of expected.
    """
    assert human_size(test_arg) == expected

    args_with_negative = -test_arg
    assert human_size(args_with_negative) == f"-{expected}"


def test_get_img_ext(img: bytes) -> None:
    assert get_img_ext(img) == "png"


def test_get_font() -> None:
    assert isinstance(get_font(), ImageFont.FreeTypeFont)


def test_get_env() -> None:
    environ["TEST_KEY_1"] = "test"
    assert get_env("TEST_KEY_1") == "test"


def test_get_env_error() -> None:
    with pytest.raises(GetEnvError):
        get_env("TEST_KEY_2")
