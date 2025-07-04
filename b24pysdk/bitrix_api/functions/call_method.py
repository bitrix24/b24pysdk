from typing import Optional, Text

from ...utils.types import JSONDict, Timeout
from .call import call
from .parse_response import parse_response


def call_method(
        *,
        domain: Text,
        auth_token: Text,
        is_webhook: bool,
        api_method: Text,
        params: Optional[JSONDict] = None,
        timeout: Timeout = None,
        **kwargs,
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

    if is_webhook:
        hook_key = f"{auth_token}/"
    else:
        hook_key = ""
        params["auth"] = auth_token

    url = f"https://{domain}/rest/{hook_key}{api_method}.json"

    response = call(
        url,
        params=params,
        timeout=timeout,
        **kwargs,
    )

    return parse_response(response)
