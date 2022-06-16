#!/usr/bin/env python
import pytest

from src.py_image_uploader.util import human_size


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
    assert human_size(test_arg) == expected

    args_with_negative = test_arg * -1
    assert human_size(args_with_negative) == "-" + expected
