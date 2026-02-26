import sys
import typing
from contextlib import suppress

from b24pysdk.utils import enum as _enum

__all__ = [
    "BITRIX_PORTAL_OWNER_ID",
    "ENV_FILE",
    "HEAD_DEPARTMENT_ID",
    "LEAD_ID",
    "OAUTH_DATA_FILE",
    "OLD_DOMAIN",
    "PROFILE_ONLY_WEBHOOK_TOKEN",
    "PYTHON_VERSION",
    "SDK_NAME",
    "SORT",
    "AuthType",
]

ENV_FILE: typing.Final[typing.Text] = ".env.local"
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


# Bitrix Portal constants (override in tests/constants_local.py)

BITRIX_PORTAL_OWNER_ID: typing.Final[int] = 1
""""""

HEAD_DEPARTMENT_ID: typing.Final[int] = 67
""""""

LEAD_ID: typing.Final[int] = 59
""""""

OLD_DOMAIN: typing.Final[typing.Text] = ""
""""""

PROFILE_ONLY_WEBHOOK_TOKEN: typing.Final[typing.Text] = ""
""""""

SORT: typing.Final[int] = 123
""""""

with suppress(ImportError):
    from .constants_local import *  # noqa: F401, F403, RUF100
