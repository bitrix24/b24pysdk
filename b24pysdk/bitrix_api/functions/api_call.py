from typing import Optional, Text

from ...utils.types import JSONDict

from .call_with_retries import request
from .convert_params import convert_params
from .parse_response import parse_response

DEFAULT_TIMEOUT = 10


def api_call(
        domain: Text,
        api_method: Text,
        auth_token: Text,
        params: Optional[JSONDict] = None,
        is_webhook: bool = False,
        timeout: int = DEFAULT_TIMEOUT,
) -> JSONDict:
    """send POST reuqest to bitrix API

    Args:
        domain: bitrix portal domain
        api_method: name of the API method (task.item.add)
        auth_token: user token
        params: dict of method parameters
        is_webhook: is method called via webhook?
        timeout: default is 10 seconds, pass None to disable timeout

    Returns:
        response of sent request
    """

    if not params:
        params = {}

    if is_webhook:
        hook_key = f"{auth_token}/"
    else:
        hook_key = ""
        params["auth"] = auth_token

    converted_params = convert_params(params).encode("utf-8")
    url = f"https://{domain}/rest/{hook_key}{api_method}.json"

    response = request(url, params=converted_params, timeout=timeout)

    return parse_response(response)
