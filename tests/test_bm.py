#!/usr/bin/env python
import pytest
from click.testing import CliRunner
from images_upload_cli.__main__ import cli


@pytest.fixture()
def runner():
    return CliRunner()


@pytest.mark.benchmark(max_time=3)
def test_bm_cli(benchmark, runner: CliRunner):
    @benchmark
    def result():
        return runner.invoke(cli=cli, args="--help")

    assert result.exit_code == 0
