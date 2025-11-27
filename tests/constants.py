import typing

from b24pysdk.utils import enum as _enum

__all__ = [
    "ENV_FILE",
    "OAUTH_DATA_FILE",
    "SDK_NAME",
    "AuthType",
]

ENV_FILE: typing.Final[typing.Text] = ".env.local"
""""""

OAUTH_DATA_FILE: typing.Final[typing.Text] = "tests/oauth_data.json"
""""""

SDK_NAME: typing.Final[typing.Text] = "B24PySDK"
""""""


class AuthType(_enum.StrEnum):
    """"""
    EMPTY = ""
    OAUTH = "oauth"
    WEBHOOK = "webhook"
