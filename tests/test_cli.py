#!/usr/bin/env python
import pytest
from click.testing import CliRunner
from images_upload_cli.__main__ import cli
from images_upload_cli.upload import HOSTINGS


@pytest.fixture()
def runner():
    return CliRunner()


@pytest.mark.parametrize(
    "args",
    [
        pytest.param(["--help"], id="help"),
        pytest.param(
            ["tests/data/pic.png", "-C", "-h", "uploadcare", "--thumbnail", "--notify"],
            id="uploadcare,thumbnail",
        ),
    ],
)
def test_cli(runner: CliRunner, args: list[str]) -> None:
    """
    Test the cli function with the provided arguments.

    Args:
        runner (CliRunner): An instance of CliRunner used to invoke the cli function.
        args (list[str]): A list of command-line arguments to be passed to the cli function.

    Raises:
        AssertionError: If the exit code of the cli function invocation is not 0.
    """
    assert runner.invoke(cli=cli, args=args).exit_code == 0


@pytest.mark.online()
@pytest.mark.parametrize(
    "args",
    [
        pytest.param(["tests/data/pic.png", "-C", "-h", hosting], id=hosting)
        for hosting in HOSTINGS
    ],
)
def test_cli_all(runner: CliRunner, args: list[str]) -> None:
    """
    Test the cli function with the provided arguments.

    Args:
        runner (CliRunner): An instance of CliRunner used to invoke the cli function.
        args (list[str]): A list of command-line arguments to be passed to the cli function.

    Raises:
        AssertionError: If the exit code of the cli function invocation is not 0.
    """
    assert runner.invoke(cli=cli, args=args).exit_code == 0
