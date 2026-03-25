import sys
import typing
from contextlib import suppress

from b24pysdk.utils import enum as _enum

__all__ = [
    "APP_NOT_FOUND_TOKEN",
    "APP_NOT_INSTALLED_TOKEN",
    "BITRIX_PORTAL_OWNER_ID",
    "DELETED_APP_REFRESH_TOKEN",
    "ENV_FILE",
    "EXTERNAL_USER_WEBHOOK_TOKEN",
    "FIRED_USER_TOKEN",
    "HEAD_DEPARTMENT_ID",
    "LEAD_ID",
    "OAUTH_DATA_FILE",
    "OLD_DOMAIN",
    "PERMISSIONS_REMOVED_REFRESH_TOKEN",
    "PROFILE_ONLY_WEBHOOK_TOKEN",
    "PYTHON_VERSION",
    "RESTRICTED_USER_OAUTH_TOKEN",
    "RESTRICTED_USER_REFRESH_TOKEN",
    "SDK_NAME",
    "SORT",
    "SUBSCRIPTION_ENDED_TOKEN",
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
"""Bitrix user ID of the portal owner account used in tests."""

HEAD_DEPARTMENT_ID: typing.Final[int] = 67
"""ID of the root (head) department in the test Bitrix portal."""

LEAD_ID: typing.Final[int] = 59
"""Existing CRM lead ID used as a stable fixture in tests."""

OLD_DOMAIN: typing.Final[typing.Text] = ""
"""Legacy portal domain used in migration or redirect-related tests."""

FIRED_USER_TOKEN: typing.Final[typing.Text] = ""
"""Webhook token of a deactivated user used to trigger auth-related API errors."""

APP_NOT_INSTALLED_TOKEN: typing.Final[typing.Text] = ""
"""Webhook token that causes Bitrix API to respond with an 'application not installed' error."""

APP_NOT_FOUND_TOKEN: typing.Final[typing.Text] = ""
"""Webhook token that causes Bitrix API to respond with an 'application not found' error."""

SUBSCRIPTION_ENDED_TOKEN: typing.Final[typing.Text] = ""
"""Webhook token for a portal whose subscription has expired."""

PROFILE_ONLY_WEBHOOK_TOKEN: typing.Final[typing.Text] = ""
"""Webhook token limited to profile scope for permission-related tests."""

EXTERNAL_USER_WEBHOOK_TOKEN: typing.Final[typing.Text] = ""
"""Webhook token of an external (extranet) user used to trigger ALLOWED_ONLY_INTRANET_USER."""

RESTRICTED_USER_OAUTH_TOKEN: typing.Final[typing.Text] = ""
"""OAuth access token for a user/app combination with restricted app access to trigger USER_ACCESS_ERROR."""

RESTRICTED_USER_REFRESH_TOKEN: typing.Final[typing.Text] = ""
"""OAuth refresh token of a user blocked from the app; refreshing should raise USER_ACCESS_ERROR."""

PERMISSIONS_REMOVED_REFRESH_TOKEN: typing.Final[typing.Text] = ""
"""OAuth refresh token for an app with removed method scopes; refreshing should still succeed."""

DELETED_APP_REFRESH_TOKEN: typing.Final[typing.Text] = ""
"""OAuth refresh token for a fully deleted app; refreshing should raise WRONG_CLIENT."""

SORT: typing.Final[int] = 123
"""Deterministic sort value used in test entities and payloads."""

with suppress(ImportError):
    from .constants_local import *  # noqa: F401, F403, RUF100
