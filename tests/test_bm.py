import pytest
from click.testing import CliRunner, Result
from dotenv import load_dotenv
from images_upload_cli.__main__ import cli
from pytest_benchmark.fixture import BenchmarkFixture
from pytest_httpx import HTTPXMock

from tests.mock import uploadcare


@pytest.fixture()
def runner():
    return CliRunner()


@pytest.mark.online()
@pytest.mark.benchmark(max_time=2)
def test_bm_cli_online(benchmark: BenchmarkFixture, runner: CliRunner):
    """Benchmark test for the cli function.

    Measures the execution time of the `cli` function using the `pytest_benchmark` library.

    Args:
        benchmark (BenchmarkFixture): A fixture provided by the `pytest_benchmark` library for benchmarking tests.
        runner (CliRunner): An instance of the `CliRunner` class from the `click.testing` module.
    """

    @benchmark
    def result() -> Result:
        """Measure the execution time of the cli function."""
        args = [
            "-h",
            "uploadcare",
            "tests/data/pic.png",
            "tests/data/pic.png",
            "tests/data/pic.png",
            "tests/data/pic.png",
            "tests/data/pic.png",
            "tests/data/pic.png",
        ]
        return runner.invoke(cli, args)

    assert result.exit_code == 0


@pytest.mark.benchmark(max_time=2)
def test_bm_cli(benchmark: BenchmarkFixture, runner: CliRunner, httpx_mock: HTTPXMock):
    """Benchmark test for the cli function.

    Measures the execution time of the `cli` function using the `pytest_benchmark` library and a mock HTTP response.

    Args:
        benchmark (BenchmarkFixture): A fixture provided by the `pytest_benchmark` library for benchmarking tests.
        runner (CliRunner): An instance of the `CliRunner` class from the `click.testing` module.
        httpx_mock (HTTPXMock): A fixture provided by the `pytest_httpx` library for mocking HTTP responses.
    """
    # Mock the response
    httpx_mock.add_response(text=uploadcare)

    # Load environment variables
    load_dotenv(dotenv_path="tests/data/.env.sample")

    @benchmark
    def result() -> Result:
        """Measure the execution time of the cli function."""
        args = [
            "-h",
            "uploadcare",
            "tests/data/pic.png",
            "tests/data/pic.png",
            "tests/data/pic.png",
            "tests/data/pic.png",
            "tests/data/pic.png",
            "tests/data/pic.png",
        ]
        return runner.invoke(cli, args)

    # Assert the exit code of the result.
    assert result.exit_code == 0
