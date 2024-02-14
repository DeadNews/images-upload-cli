from os import environ
from unittest.mock import MagicMock, patch

import pytest
from images_upload_cli.util import (
    GetEnvError,
    get_env,
    human_size,
    notify_send,
)


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
    """
    Test the human_size function.

    Args:
        test_arg (int): The number of bytes to be converted.
        expected (str): The expected human-readable size with the appropriate unit and suffix.

    Raises:
        AssertionError: If the output of calling human_size with (negation of) test_arg is not equal to (negation of) expected.
    """
    assert human_size(test_arg) == expected

    args_with_negative = -test_arg
    assert human_size(args_with_negative) == f"-{expected}"


def test_get_env() -> None:
    environ["TEST_KEY_1"] = "test"
    assert get_env("TEST_KEY_1") == "test"


def test_get_env_error() -> None:
    with pytest.raises(GetEnvError):
        get_env("TEST_KEY_2")


def test_notify_send_with_notify_send_installed_(mocker):
    """
    Test the notify_send function when notify-send is installed.
    """
    which_mock = mocker.patch("images_upload_cli.util.which", return_value="notify-send")
    popen_mock = mocker.patch("images_upload_cli.util.Popen")

    notify_send("Test notification")

    # Check if the which function was called with the correct argument
    which_mock.assert_called_once_with("notify-send")

    # Check if the Popen function was called with the correct arguments
    popen_mock.assert_called_once_with(
        ["notify-send", "-a", "images-upload-cli", "Test notification"]
    )


def test_notify_send_with_notify_send_not_installed_(mocker):
    """
    Test the notify_send function when notify-send is not installed.
    """
    which_mock = mocker.patch("images_upload_cli.util.which", return_value=None)
    popen_mock = mocker.patch("images_upload_cli.util.Popen")

    notify_send("Test notification")

    # Check if the which function was called with the correct argument
    which_mock.assert_called_once_with("notify-send")

    # Check if the Popen function was not called
    popen_mock.assert_not_called()


@patch("images_upload_cli.util.which", return_value="notify-send")
@patch("images_upload_cli.util.Popen")
def test_notify_send_with_notify_send_installed(popen_mock: MagicMock, which_mock: MagicMock):
    """
    Test the notify_send function when notify-send is installed.
    """
    notify_send("Test notification")

    # Check if the which function was called with the correct argument
    which_mock.assert_called_once_with("notify-send")

    # Check if the Popen function was called with the correct arguments
    popen_mock.assert_called_once_with(
        ["notify-send", "-a", "images-upload-cli", "Test notification"]
    )


@patch("images_upload_cli.util.which", return_value=None)
@patch("images_upload_cli.util.Popen")
def test_notify_send_with_notify_send_not_installed(popen_mock: MagicMock, which_mock: MagicMock):
    """
    Test the notify_send function when notify-send is not installed.
    """
    notify_send("Test notification")

    # Check if the which function was called with the correct argument
    which_mock.assert_called_once_with("notify-send")

    # Check if the Popen function was not called
    popen_mock.assert_not_called()
