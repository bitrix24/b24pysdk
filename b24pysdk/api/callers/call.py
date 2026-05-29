from typing import IO, Dict, Optional, Text, Tuple

from ...utils.types import JSONDict, Number, Timeout
from ..requesters import BitrixAPIRequester

__all__ = [
    "call",
]


def call(
        url: Text,
        *,
        params: Optional[JSONDict] = None,
        files: Optional[Dict[Text, Tuple[Text, IO]]] = None,
        timeout: Timeout = None,
        max_retries: Optional[int] = None,
        initial_retry_delay: Optional[Number] = None,
        retry_delay_increment: Optional[Number] = None,
) -> JSONDict:
    """
    Perform one HTTP request to a concrete Bitrix REST URL.

    This is the lowest-level caller in the SDK. It does not know which Bitrix
    method is being called and does not add authentication by itself; callers
    above this function build the URL and parameters first. The function
    delegates request execution, retry handling, and response parsing to
    ``BitrixAPIRequester``.

    Args:
        url: Absolute Bitrix REST endpoint URL.
        params: Request parameters sent in the request body.
        files: Files attached to the request.
        timeout: Request timeout in seconds.
        max_retries: Maximum retry attempts for transport-level failures.
        initial_retry_delay: Delay before the first retry, in seconds.
        retry_delay_increment: Increment added to retry delay after each retry.

    Returns:
        Parsed JSON response returned by the Bitrix API server.

    Raises:
        BitrixRequestError: If the HTTP connection cannot be established.
        BitrixRequestTimeout: If the request times out.
    """
    return BitrixAPIRequester(
        url=url,
        params=params,
        files=files,
        timeout=timeout,
        max_retries=max_retries,
        initial_retry_delay=initial_retry_delay,
        retry_delay_increment=retry_delay_increment,
    ).call()
