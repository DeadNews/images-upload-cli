"""Shared fixtures."""

from pathlib import Path

import pytest


@pytest.fixture()
def img() -> bytes:
    return Path("tests/data/pic.png").read_bytes()
