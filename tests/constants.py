import sys
import typing
from contextlib import suppress

from b24pysdk.utils import enum as _enum

__all__ = [
    "BITRIX_PORTAL_OWNER_ID",
    "ENV_FILE",
    "HEAD_DEPARTMENT_ID",
    "OAUTH_DATA_FILE",
    "PYTHON_VERSION",
    "SDK_NAME",
    "AuthType",
]


ENV_FILE: typing.Final[typing.Text] = ".env.local"
""""""

HEAD_DEPARTMENT_ID: typing.Final[int] = 67
""""""

BITRIX_PORTAL_OWNER_ID: typing.Final[int] = 1
""""""

OAUTH_DATA_FILE: typing.Final[typing.Text] = "tests/oauth_data.json"
""""""

PYTHON_VERSION: typing.Final[typing.Tuple] = sys.version_info
""""""

SDK_NAME: typing.Final[typing.Text] = "B24PySDK"
""""""


class AuthType(_enum.StrEnum):
    """"""
    EMPTY = ""
    OAUTH = "oauth"
    WEBHOOK = "webhook"


with suppress(ImportError):
    from .constants_local import *  # noqa: F403
