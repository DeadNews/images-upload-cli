#!/usr/bin/env python
"""Shared fixtures."""

from pathlib import Path

import pytest


@pytest.fixture()
def img() -> bytes:
    return Path("tests/resources/pic.png").read_bytes()
