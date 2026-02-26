from abc import ABC
from dataclasses import asdict, dataclass
from typing import TYPE_CHECKING, Any, List, Mapping, Optional, Text
from urllib.parse import urlparse

from .._constants import PYTHON_VERSION
from ..constants import B24AppStatus
from ..error import BitrixValidationError
from ..utils.types import JSONDict
from .oauth_token import OAuthToken

if TYPE_CHECKING:
    from ..api.responses import B24AppInfoResult

__all__ = [
    "EventOAuth",
    "RenewedOAuth",
    "WorkflowOAuth",
]

_DATACLASS_KWARGS = {"eq": False, "frozen": True}

if PYTHON_VERSION >= (3, 10):
    _DATACLASS_KWARGS["slots"] = True


@dataclass(**_DATACLASS_KWARGS)
class Auth(ABC):
    """Base authentication payload returned by Bitrix24 events.

    This model captures the common fields present in all event auth payloads.
    """

    class ValidationError(BitrixValidationError):
        """"""

    member_id: Text
    client_endpoint: Text
    server_endpoint: Text
    domain: Text

    @classmethod
    def _validate_payload(cls, payload: Mapping[Text, Any], /) -> JSONDict:
        return {
            "member_id": payload["member_id"],
            "client_endpoint": payload["client_endpoint"],
            "server_endpoint": payload["server_endpoint"],
            "domain": payload["domain"],
        }

    @classmethod
    def from_dict(cls, payload: Mapping[Text, Any], /) -> "Auth":
        try:
            return cls(**cls._validate_payload(payload))
        except KeyError as error:
            raise cls.ValidationError(f"Missing required field in Auth payload: {error.args[0]}") from error
        except Exception as error:
            raise cls.ValidationError(f"Invalid Auth payload: {error}") from error

    @property
    def portal_domain(self) -> Text:
        """Return the portal domain derived from the client endpoint URL."""
        return urlparse(self.client_endpoint).hostname

    def validate_against_app_info(self, app_info: "B24AppInfoResult") -> bool:
        """Validate auth data against Bitrix24 application info."""
        if all((
                self.member_id == app_info.install.member_id,
                self.portal_domain == app_info.install.domain,
        )):
            return True
        else:
            raise self.ValidationError("Invalid auth")

    def to_dict(self) -> JSONDict:
        """"""
        return asdict(self)


@dataclass(**_DATACLASS_KWARGS)
class EventOAuth(Auth):
    """OAuth payload for Bitrix24 events with optional user context.

    OAuth fields may be absent for system events executed without a user.
    """

    application_token: Text
    oauth_token: Optional[OAuthToken] = None
    user_id: Optional[int] = None
    scope: Optional[List[Text]] = None
    status: Optional[B24AppStatus] = None

    @classmethod
    def _validate_payload(cls, payload: Mapping[Text, Any], /) -> JSONDict:
        oauth_token = OAuthToken.from_dict(payload) if payload.get("access_token") else None

        scope_value = payload.get("scope")
        scope = scope_value.split(",") if scope_value is not None else None

        status_value = payload.get("status")
        status = B24AppStatus(status_value) if status_value is not None else None

        return super(EventOAuth, cls)._validate_payload(payload) | {
            "application_token": payload["application_token"],
            "oauth_token": oauth_token,
            "user_id": int(payload["user_id"]) if payload.get("user_id") is not None else None,
            "scope": scope,
            "status": status,
        }

    @classmethod
    def from_dict(cls, payload: Mapping[Text, Any], /) -> "EventOAuth":
        try:
            return cls(**cls._validate_payload(payload))
        except KeyError as error:
            raise cls.ValidationError(f"Missing required field in event OAuth payload: {error.args[0]}") from error
        except Exception as error:
            raise cls.ValidationError(f"Invalid event OAuth payload: {error}") from error

    @property
    def is_system(self) -> bool:
        """Return True when the event has no user OAuth context."""
        return not bool(self.oauth_token)

    def validate_against_app_info(self, app_info: "B24AppInfoResult") -> bool:
        """Validate event auth data against Bitrix24 application info."""
        if all((
                super(EventOAuth, self).validate_against_app_info(app_info),
                self.user_id is None or self.user_id == app_info.user_id,
        )):
            return True
        else:
            raise self.ValidationError("Invalid event OAuth")


@dataclass(**_DATACLASS_KWARGS)
class RenewedOAuth(Auth):
    """OAuth payload returned after refreshing an access token."""

    oauth_token: OAuthToken
    user_id: int
    scope: List[Text]
    status: B24AppStatus

    @classmethod
    def _validate_payload(cls, payload: Mapping[Text, Any], /) -> JSONDict:
        return super(RenewedOAuth, cls)._validate_payload(payload) | {
            "oauth_token": OAuthToken.from_dict(payload),
            "user_id": int(payload["user_id"]),
            "scope": payload["scope"].split(","),
            "status": B24AppStatus(payload["status"]),
        }

    @classmethod
    def from_dict(cls, payload: Mapping[Text, Any], /) -> "RenewedOAuth":
        try:
            return cls(**cls._validate_payload(payload))
        except KeyError as error:
            raise cls.ValidationError(f"Missing required field in renewed OAuth payload: {error.args[0]}") from error
        except Exception as error:
            raise cls.ValidationError(f"Invalid renewed OAuth payload: {error}") from error

    def validate_against_app_info(self, app_info: "B24AppInfoResult") -> bool:
        """Validate refreshed OAuth data against Bitrix24 application info."""
        if all((
                super(RenewedOAuth, self).validate_against_app_info(app_info),
                self.user_id == app_info.user_id,
        )):
            return True
        else:
            raise self.ValidationError("Invalid renewed OAuth")


@dataclass(**_DATACLASS_KWARGS)
class WorkflowOAuth(RenewedOAuth):
    """OAuth payload for workflow robot events in business processes."""

    application_token: Text

    @classmethod
    def _validate_payload(cls, payload: Mapping[Text, Any], /) -> JSONDict:
        return super(WorkflowOAuth, cls)._validate_payload(payload) | {"application_token": payload["application_token"]}

    @classmethod
    def from_dict(cls, payload: Mapping[Text, Any], /) -> "WorkflowOAuth":
        try:
            return cls(**cls._validate_payload(payload))
        except KeyError as error:
            raise cls.ValidationError(f"Missing required field in workflow OAuth payload: {error.args[0]}") from error
        except Exception as error:
            raise cls.ValidationError(f"Invalid workflow OAuth payload: {error}") from error

    def validate_against_app_info(self, app_info: "B24AppInfoResult") -> bool:
        """Validate workflow OAuth data against Bitrix24 application info."""
        try:
            return super(WorkflowOAuth, self).validate_against_app_info(app_info)
        except self.ValidationError as error:
            raise self.ValidationError("Invalid workflow OAuth") from error
