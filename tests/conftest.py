"""Shared fixtures."""

from pathlib import Path
from typing import Callable

import pytest
from logot.loguru import LoguruCapturer


@pytest.fixture()
def img() -> bytes:
    return Path("tests/data/pic.png").read_bytes()


@pytest.fixture(scope="session")
def logot_capturer() -> Callable[[], LoguruCapturer]:
    return LoguruCapturer
