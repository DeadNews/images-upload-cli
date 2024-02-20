from pathlib import Path

import pytest
from httpx import codes, post
from images_upload_cli.util import (
    GetEnvError,
    get_config_path,
    get_env,
    human_size,
    log_on_error,
    notify_send,
)
from logot import Logot, logged
from pytest_httpx import HTTPXMock
from pytest_mock import MockerFixture


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
    """Test the human_size function.

    Args:
        test_arg: The number of bytes to be converted.
        expected: The expected human-readable size with the appropriate unit and suffix.

    Raises:
        AssertionError: If the output of calling human_size with (negation of) test_arg is not equal to (negation of) expected.
    """
    assert human_size(test_arg) == expected

    args_with_negative = -test_arg
    assert human_size(args_with_negative) == f"-{expected}"


def test_get_config_path(mocker: MockerFixture):
    """Test the get_config_path function."""
    # Mock the click.get_app_dir function to return a custom app directory
    custom_app_dir = "/custom/app/dir"
    click_get_app_dir_mock = mocker.patch("click.get_app_dir", return_value=custom_app_dir)

    # Call the get_config_path function
    result = get_config_path()

    # Check if the click.get_app_dir function was called with the correct argument
    click_get_app_dir_mock.assert_called_once_with("images-upload-cli")

    # Check if the result is the expected path
    expected_path = Path(custom_app_dir) / ".env"
    assert result == expected_path


def test_get_env_existing_variable(mocker: MockerFixture):
    """Test the get_env function with an existing environment variable."""
    variable = "TEST_VARIABLE"
    value = "test_value"
    mocker.patch.dict("os.environ", {variable: value})

    assert get_env(variable) == value


def test_get_env_non_existing_variable(mocker: MockerFixture):
    """Test the get_env function with a non-existing environment variable."""
    variable = "NON_EXISTING_VARIABLE"
    mocker.patch.dict("os.environ", clear=True)

    with pytest.raises(GetEnvError):
        get_env(variable)


def test_notify_send_with_notify_send_installed(mocker: MockerFixture):
    """Test the notify_send function when notify-send is installed."""
    which_mock = mocker.patch("images_upload_cli.util.which", return_value="notify-send")
    popen_mock = mocker.patch("images_upload_cli.util.Popen")

    notify_send("Test notification")

    # Check if the which function was called with the correct argument
    which_mock.assert_called_once_with("notify-send")

    # Check if the Popen function was called with the correct arguments
    popen_mock.assert_called_once_with(
        ["notify-send", "-a", "images-upload-cli", "Test notification"]
    )


def test_notify_send_with_notify_send_not_installed(mocker: MockerFixture):
    """Test the notify_send function when notify-send is not installed."""
    which_mock = mocker.patch("images_upload_cli.util.which", return_value=None)
    popen_mock = mocker.patch("images_upload_cli.util.Popen")

    notify_send("Test notification")

    # Check if the which function was called with the correct argument
    which_mock.assert_called_once_with("notify-send")

    # Check if the Popen function was not called
    popen_mock.assert_not_called()


def test_log_on_error(httpx_mock: HTTPXMock, logot: Logot):
    """Test the log_on_error function when a client error occurs.

    Args:
        httpx_mock: The HTTPXMock object for mocking HTTP requests.
        logot: The Logot object for logging.
    """
    # Mock the response
    httpx_mock.add_response(status_code=codes.NOT_FOUND, text="Page not found")

    response = post(url="https://example.com")
    log_on_error(response)

    # Assert the log messages
    logot.assert_logged(
        logged.error("Client error '404 Not Found' for url 'https://example.com'.")
    )
    logot.assert_logged(logged.debug("Response text:\nPage not found"))
