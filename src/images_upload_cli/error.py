"""Error handling and exception classes."""
from httpx import HTTPError, Response


class GetEnvError(Exception):
    """Exception raised when an environment variable is not found."""


def raise_on_error(response: Response) -> None:
    """
    Raise an exception if the response status is not a success.

    Args:
        response (Response): The HTTP response object.

    Raises:
        HTTPError: If the response status code indicates an error.
    """
    if not response.is_success:
        status_class = response.status_code // 100
        error_types = {
            1: "Informational response",
            3: "Redirect response",
            4: "Client error",
            5: "Server error",
        }
        error_type = error_types.get(status_class, "Invalid status code")

        msg = (
            f"{error_type} '{response.status_code} {response.reason_phrase}'"
            f" for url '{response.url}'. Response text below:\n"
            f"\n{response.text}"
        )
        raise HTTPError(msg)
