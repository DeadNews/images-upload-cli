#!/usr/bin/env python
from __future__ import annotations

from typing import TYPE_CHECKING

import httpx
import pytest
from dotenv import load_dotenv
from images_upload_cli.upload import HOSTINGS, UPLOAD

from tests.fixture import RESPONSE, img  # noqa: F401

if TYPE_CHECKING:
    from pytest_httpx import HTTPXMock


@pytest.mark.parametrize(
    ("hosting", "mock_text", "mock_link"),
    [
        pytest.param(hosting, RESPONSE[hosting][0], RESPONSE[hosting][1], id=hosting)
        for hosting in HOSTINGS
    ],
)
@pytest.mark.asyncio()
async def test_upload(
    httpx_mock: HTTPXMock,
    hosting: str,
    mock_text: str,
    mock_link: str,
    img: bytes,  # noqa: F811
):
    httpx_mock.add_response(text=mock_text)

    # loading .env variables
    load_dotenv(dotenv_path="tests/resources/test.env")

    # images upload
    async with httpx.AsyncClient() as client:
        upload_func = UPLOAD[hosting]
        link = await upload_func(client, img)
        assert link == mock_link
