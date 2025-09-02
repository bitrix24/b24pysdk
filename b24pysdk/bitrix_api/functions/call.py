from typing import IO, Dict, Optional, Text, Tuple

import requests

from ...utils.types import JSONDict, Timeout
from ..requesters import BitrixApiRequester


def call(
        url: Text,
        *,
        params: Optional[JSONDict] = None,
        files: Optional[Dict[Text, Tuple[Text, IO]]] = None,
        timeout: Timeout = None,
        max_retries: Optional[int] = None,
        initial_retry_delay: Optional[float] = None,
        retry_delay_increment: Optional[float] = None,
) -> requests.Response:
    """
    Performs a call to the Bitrix API

    Args:
        url: url to which the request should be sent
        params: API method parameters
        files: files attached to the request
        timeout: timeout in seconds
        max_retries: maximum number of retries that will occur when server is not responding
        initial_retry_delay: initial delay between retries in seconds
        retry_delay_increment: amount by which delay between retries will increment after each retry

    Returns:
        Response returned by the API server
    Raises:
            BitrixRequestError: if failed to establish HTTP connection
            BitrixTimeout: if the request timed out
    """
    return BitrixApiRequester(
        url=url,
        params=params,
        files=files,
        timeout=timeout,
        max_retries=max_retries,
        initial_retry_delay=initial_retry_delay,
        retry_delay_increment=retry_delay_increment,
    ).call()
