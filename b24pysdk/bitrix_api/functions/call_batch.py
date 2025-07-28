from typing import Dict, Sequence, Text, Union

from ...utils.encoding import encode_params
from ...utils.types import B24BatchRequestData, JSONDict, Key, Timeout
from .call_method import call_method

MAX_BATCH_SIZE = 50
API_METHOD = "batch"


def call_batch(
        *,
        domain: Text,
        auth_token: Text,
        is_webhook: bool,
        methods: Union[Dict[Key, B24BatchRequestData], Sequence[B24BatchRequestData]],
        halt: bool = False,
        ignore_size_limit: bool = False,
        timeout: Timeout = None,
        **kwargs,
) -> JSONDict:
    """"""

    if len(methods) > MAX_BATCH_SIZE:
        if ignore_size_limit:
            methods = methods[:MAX_BATCH_SIZE]
        else:
            raise ValueError(f"Maximum batch size is {MAX_BATCH_SIZE}!")

    cmd: Dict[Key, Text] = dict()

    if isinstance(methods, dict):
        for key, (api_method, params) in methods.items():
            cmd[key] = f"{api_method}?{encode_params(params)}"
    else:
        for index, (api_method, params) in enumerate(methods):
            cmd[index] = f"{api_method}?{encode_params(params)}"

    return call_method(
            domain=domain,
            auth_token=auth_token,
            is_webhook=is_webhook,
            api_method=API_METHOD,
            params=dict(
                cmd=cmd,
                halt=halt,
            ),
            timeout=timeout,
            **kwargs,
    )
