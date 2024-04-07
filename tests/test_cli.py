import pytest
from click.testing import CliRunner
from images_upload_cli.__main__ import cli
from images_upload_cli.upload import HOSTINGS
from pytest_httpx import HTTPXMock
from pytest_mock import MockerFixture

from tests.mock import MOCK_HOSTINGS, RESPONSE


@pytest.fixture()
def runner():
    return CliRunner()


def test_cli_help(runner: CliRunner) -> None:
    """Test the cli function with the provided arguments."""
    args = ["--help"]
    assert runner.invoke(cli=cli, args=args).exit_code == 0


def test_cli_error(runner: CliRunner) -> None:
    """Test the cli function with the provided arguments."""
    args = ["tests/data/nonexistent", "-C", "-h", "nonexistent"]
    assert runner.invoke(cli=cli, args=args).exit_code == 2


@pytest.mark.parametrize(
    ("hosting", "mock_text", "mock_link"),
    [
        pytest.param(hosting, RESPONSE[hosting][0], RESPONSE[hosting][1], id=hosting)
        for hosting in MOCK_HOSTINGS
    ],
)
@pytest.mark.parametrize(
    "thumbnail",
    [pytest.param(False, id="default"), pytest.param(True, id="thumbnail")],
)
def test_cli(
    runner: CliRunner,
    httpx_mock: HTTPXMock,
    mocker: MockerFixture,
    hosting: str,
    mock_text: str,
    mock_link: str,
    thumbnail: bool,
) -> None:
    """Test the cli function with different hosting services.

    Args:
        runner: An instance of CliRunner used to invoke the cli function.
        httpx_mock: An instance of HTTPXMock used to mock the HTTP responses.
        mocker: An instance of MockerFixture used for mocking.
        hosting: The hosting service to use for image upload.
        mock_text: The mock response text to be returned by the HTTPXMock.
        mock_link: The expected link to be returned by the cli function.
        thumbnail: Flag indicating whether to generate a thumbnail link.
    """
    # Mock response.
    httpx_mock.add_response(text=mock_text)
    # Mock functions.
    mock_copy = mocker.patch("images_upload_cli._cli.copykitten.copy", return_value=None)
    mock_notify_send = mocker.patch("images_upload_cli._cli.notify_send", return_value=None)
    # Mock image extension to be matched with mock_link.
    mocker.patch("images_upload_cli.upload.get_img_ext", return_value="png")

    # Thumbnail link.
    mock_link_thumb = f"[url={mock_link}][img]{mock_link}[/img][/url]"

    # Invoke the cli function.
    args = [
        "tests/data/pic.png",
        "--env-file",
        "tests/data/.env.sample",
        "--notify",
        "-h",
        hosting,
    ]
    if thumbnail:
        args.append("--thumbnail")

    result = runner.invoke(cli=cli, args=args)

    # Assert the result.
    assert result.exit_code == 0

    if thumbnail:
        assert result.output.strip() == mock_link_thumb
        mock_copy.assert_called_once_with(mock_link_thumb)
        mock_notify_send.assert_called_once_with(mock_link_thumb)
    else:
        assert result.output.strip() == mock_link
        mock_copy.assert_called_once_with(mock_link)
        mock_notify_send.assert_called_once_with(mock_link)


@pytest.mark.online()
@pytest.mark.parametrize("hosting", HOSTINGS)
def test_cli_online(runner: CliRunner, hosting: str) -> None:
    """
    Test the cli function with different hosting services. Online.

    Args:
        runner: An instance of CliRunner used to invoke the cli function.
        hosting: The hosting service to be tested.
    """
    args = ["tests/data/pic.png", "-C", "-h", hosting]
    assert runner.invoke(cli=cli, args=args).exit_code == 0
