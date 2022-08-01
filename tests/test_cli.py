#!/usr/bin/env python
from pathlib import Path

import pytest
from click.testing import CliRunner

from src.image_upload_cli.cli import cli

from .img import img


@pytest.fixture()
def img_path(tmp_path) -> str:
    target_img = Path(f"{tmp_path}/img.png")
    target_img.write_bytes(img)
    return f"{target_img}"


@pytest.fixture()
def runner() -> CliRunner:
    return CliRunner()


# @pytest.mark.parametrize(
#     argnames=("args"),
#     argvalues=[
#         (["--help"]),
#         (["img_path", "--no-clipboard", "-h", "imgur"]),
#         (["img_path", "--no-clipboard", "-h", "pixhost"]),
#         (["img_path", "--no-clipboard", "-h", "uploadcare"]),
#     ],
#     # indirect=["img_path"],
# )
def test_help(runner):
    assert runner.invoke(cli, ["--help"]).exit_code == 0


# def test_imgur(runner, img_path):
#     assert (
#         runner.invoke(cli, [img_path, "--no-clipboard", "-h", "imgur"]).exit_code == 0
#     )


# def test_pixhost(runner, img_path):
#     assert (
#         runner.invoke(cli, [img_path, "--no-clipboard", "-h", "pixhost"]).exit_code == 0
#     )


def test_uploadcare(runner, img_path):
    assert (
        runner.invoke(
            cli,
            [img_path, "--no-clipboard", "-h", "pixhost", "--thumbnail"],
        ).exit_code
        == 0
    )
