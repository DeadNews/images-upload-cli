#!/usr/bin/env python
import pytest
from click.testing import CliRunner
from dotenv import load_dotenv
from images_upload_cli.__main__ import cli
from pytest_httpx import HTTPXMock

from tests.mock import uploadcare


@pytest.fixture()
def runner():
    return CliRunner()


@pytest.mark.online()
@pytest.mark.benchmark(max_time=2)
def test_bm_cli_online(benchmark, runner: CliRunner):
    @benchmark
    def result():
        return runner.invoke(
            cli=cli,
            args=[
                "-h",
                "uploadcare",
                "tests/data/pic.png",
                "tests/data/pic.png",
                "tests/data/pic.png",
                "tests/data/pic.png",
                "tests/data/pic.png",
                "tests/data/pic.png",
            ],
        )

    assert result.exit_code == 0


@pytest.mark.benchmark(max_time=2)
def test_bm_cli(benchmark, runner: CliRunner, httpx_mock: HTTPXMock):
    # mock response
    httpx_mock.add_response(text=uploadcare)

    # loading .env variables
    load_dotenv(dotenv_path="tests/data/.env.sample")

    @benchmark
    def result():
        return runner.invoke(
            cli=cli,
            args=[
                "-h",
                "uploadcare",
                "tests/data/pic.png",
                "tests/data/pic.png",
                "tests/data/pic.png",
                "tests/data/pic.png",
                "tests/data/pic.png",
                "tests/data/pic.png",
            ],
        )

    assert result.exit_code == 0
