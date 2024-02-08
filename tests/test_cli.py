import pytest
from click.testing import CliRunner
from images_upload_cli.__main__ import cli
from images_upload_cli.upload import HOSTINGS
from pytest_httpx import HTTPXMock

from tests.mock import MOCK_HOSTINGS, RESPONSE


@pytest.fixture()
def runner():
    return CliRunner()


def test_cli_help(runner: CliRunner) -> None:
    """
    Test the cli function with the provided arguments.

    Args:
        runner (CliRunner): An instance of CliRunner used to invoke the cli function.
    """
    args = ["--help"]
    assert runner.invoke(cli=cli, args=args).exit_code == 0


def test_cli_error(runner: CliRunner) -> None:
    """
    Test the cli function with the provided arguments.

    Args:
        runner (CliRunner): An instance of CliRunner used to invoke the cli function.
    """
    args = ["tests/data/nonexistent.png", "-C", "-h", "uploadcare"]
    assert runner.invoke(cli=cli, args=args).exit_code == 2


@pytest.mark.parametrize(
    ("hosting", "mock_text", "mock_link"),
    [
        pytest.param(hosting, RESPONSE[hosting][0], RESPONSE[hosting][1], id=hosting)
        for hosting in MOCK_HOSTINGS
    ],
)
def test_cli(
    runner: CliRunner,
    httpx_mock: HTTPXMock,
    hosting: str,
    mock_text: str,
    mock_link: str,
) -> None:
    """
    Test the cli function with different hosting services.

    Args:
        runner (CliRunner): An instance of CliRunner used to invoke the cli function.
        httpx_mock (HTTPXMock): An instance of HTTPXMock used to mock the HTTP responses.
        hosting (str): The hosting service to use for image upload.
        mock_text (str): The mock response text to be returned by the HTTPXMock.
        mock_link (str): The expected link to be returned by the cli function.
    """
    # Mock the response.
    httpx_mock.add_response(text=mock_text)

    # Invoke the cli function.
    args = ["tests/data/pic.png", "--env-file", "tests/data/.env.sample", "-C", "-h", hosting]
    result = runner.invoke(cli=cli, args=args)

    assert result.exit_code == 0
    assert result.output.strip() == mock_link


@pytest.mark.online()
@pytest.mark.parametrize("hosting", HOSTINGS)
def test_cli_online(runner: CliRunner, hosting: str) -> None:
    """
    Test the cli function with different hosting services. Online.

    Args:
        runner (CliRunner): An instance of CliRunner used to invoke the cli function.
        args (list[str]): A list of command-line arguments to be passed to the cli function.
    """
    args = ["tests/data/pic.png", "-C", "-h", hosting]
    assert runner.invoke(cli=cli, args=args).exit_code == 0
