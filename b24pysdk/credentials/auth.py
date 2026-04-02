from abc import ABC
from dataclasses import asdict, dataclass
from typing import TYPE_CHECKING, Any, List, Mapping, Optional, Text
from urllib.parse import urlparse

from .._constants import PYTHON_VERSION
from ..constants import B24AppStatus
from ..errors import BitrixValidationError
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
    """
    Base authentication payload returned by Bitrix24 events.

    Contains common fields shared across all event authentication payloads,
    such as portal identifiers and endpoint URLs.
    """

    class ValidationError(BitrixValidationError):
        """Raised when Auth payload validation fails."""

    member_id: Text
    client_endpoint: Text
    server_endpoint: Text
    domain: Text

    @classmethod
    def _validate_payload(cls, payload: Mapping[Text, Any], /) -> JSONDict:
        """
        Extract and validate base Auth fields from payload.

        Args:
            payload: Raw payload received from Bitrix24.

        Returns:
            Dictionary with validated base fields.

        Raises:
            KeyError: If required fields are missing.
        """
        return {
            "member_id": payload["member_id"],
            "client_endpoint": payload["client_endpoint"],
            "server_endpoint": payload["server_endpoint"],
            "domain": payload["domain"],
        }

    @classmethod
    def from_dict(cls, payload: Mapping[Text, Any], /) -> "Auth":
        """
        Create an Auth instance from payload.

        Args:
            payload: Raw payload received from Bitrix24.

        Returns:
            Auth instance.

        Raises:
            Auth.ValidationError: If validation fails.
        """
        try:
            return cls(**cls._validate_payload(payload))
        except KeyError as error:
            raise cls.ValidationError(f"Missing required field in Auth payload: {error.args[0]}") from error
        except Exception as error:
            raise cls.ValidationError(f"Invalid Auth payload: {error}") from error

    @property
    def portal_domain(self) -> Text:
        """
        Extract portal domain from the client endpoint URL.

        Returns:
            Hostname part of the client endpoint URL.
        """
        return urlparse(self.client_endpoint).hostname

    def validate_against_app_info(self, app_info: "B24AppInfoResult") -> bool:
        """
        Validate Auth data against application installation info.

        Args:
            app_info: Application info result.

        Returns:
            True if validation succeeds.

        Raises:
            Auth.ValidationError: If validation fails.
        """
        if all((
                self.member_id == app_info.install.member_id,
                self.portal_domain == app_info.install.domain,
        )):
            return True
        else:
            raise self.ValidationError("Invalid auth")

    def to_dict(self) -> JSONDict:
        """
        Convert Auth instance to dictionary.

        Returns:
            Dictionary representation of the auth payload.
        """
        return asdict(self)


@dataclass(**_DATACLASS_KWARGS)
class EventOAuth(Auth):
    """
    OAuth payload for Bitrix24 event handlers.

    May include user-related OAuth context. For system events,
    OAuth data may be absent.
    """

    application_token: Text
    oauth_token: Optional[OAuthToken] = None
    user_id: Optional[int] = None
    scope: Optional[List[Text]] = None
    status: Optional[B24AppStatus] = None

    @classmethod
    def _validate_payload(cls, payload: Mapping[Text, Any], /) -> JSONDict:
        """
        Extract and validate EventOAuth-specific fields.

        Args:
            payload: Raw event payload.

        Returns:
            Dictionary with validated EventOAuth fields.
        """

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
        """
        Create an EventOAuth instance from payload.

        Args:
            payload: Raw event payload.

        Returns:
            EventOAuth instance.

        Raises:
            EventOAuth.ValidationError: If validation fails.
        """
        try:
            return cls(**cls._validate_payload(payload))
        except KeyError as error:
            raise cls.ValidationError(f"Missing required field in event OAuth payload: {error.args[0]}") from error
        except Exception as error:
            raise cls.ValidationError(f"Invalid event OAuth payload: {error}") from error

    @property
    def is_system(self) -> bool:
        """
        Indicates whether the event was triggered without user context.

        Returns:
            True if no OAuth token is present, otherwise False.
        """
        return not bool(self.oauth_token)

    def validate_against_app_info(self, app_info: "B24AppInfoResult") -> bool:
        """
        Validate event OAuth data against application info.

        Args:
            app_info: Application info result.

        Returns:
            True if validation succeeds.

        Raises:
            EventOAuth.ValidationError: If validation fails.
        """
        if all((
                super(EventOAuth, self).validate_against_app_info(app_info),
                self.user_id is None or self.user_id == app_info.user_id,
        )):
            return True
        else:
            raise self.ValidationError("Invalid event OAuth")


@dataclass(**_DATACLASS_KWARGS)
class RenewedOAuth(Auth):
    """
    OAuth payload returned after token refresh.

    Always contains a valid OAuth token and user context.
    """

    oauth_token: OAuthToken
    user_id: int
    scope: List[Text]
    status: B24AppStatus

    @classmethod
    def _validate_payload(cls, payload: Mapping[Text, Any], /) -> JSONDict:
        """
        Extract and validate RenewedOAuth fields.

        Args:
            payload: Raw OAuth refresh response.

        Returns:
            Dictionary with validated fields.
        """
        return super(RenewedOAuth, cls)._validate_payload(payload) | {
            "oauth_token": OAuthToken.from_dict(payload),
            "user_id": int(payload["user_id"]),
            "scope": payload["scope"].split(","),
            "status": B24AppStatus(payload["status"]),
        }

    @classmethod
    def from_dict(cls, payload: Mapping[Text, Any], /) -> "RenewedOAuth":
        """
        Create a RenewedOAuth instance from payload.

        Args:
            payload: Raw OAuth refresh response.

        Returns:
            RenewedOAuth instance.

        Raises:
            RenewedOAuth.ValidationError: If validation fails.
        """
        try:
            return cls(**cls._validate_payload(payload))
        except KeyError as error:
            raise cls.ValidationError(f"Missing required field in renewed OAuth payload: {error.args[0]}") from error
        except Exception as error:
            raise cls.ValidationError(f"Invalid renewed OAuth payload: {error}") from error

    def validate_against_app_info(self, app_info: "B24AppInfoResult") -> bool:
        """
        Validate refreshed OAuth data against application info.

        Args:
            app_info: Application info result.

        Returns:
            True if validation succeeds.

        Raises:
            RenewedOAuth.ValidationError: If validation fails.
        """
        if all((
                super(RenewedOAuth, self).validate_against_app_info(app_info),
                self.user_id == app_info.user_id,
        )):
            return True
        else:
            raise self.ValidationError("Invalid renewed OAuth")


@dataclass(**_DATACLASS_KWARGS)
class WorkflowOAuth(RenewedOAuth):
    """
    OAuth payload for Bitrix24 business process (workflow) events.

    Extends RenewedOAuth with application token required for workflow execution.
    """

    application_token: Text

    @classmethod
    def _validate_payload(cls, payload: Mapping[Text, Any], /) -> JSONDict:
        """
        Extract and validate WorkflowOAuth fields.

        Args:
            payload: Raw workflow event payload.

        Returns:
            Dictionary with validated fields.
        """
        return super(WorkflowOAuth, cls)._validate_payload(payload) | {"application_token": payload["application_token"]}

    @classmethod
    def from_dict(cls, payload: Mapping[Text, Any], /) -> "WorkflowOAuth":
        """
        Create a WorkflowOAuth instance from payload.

        Args:
            payload: Raw workflow event payload.

        Returns:
            WorkflowOAuth instance.

        Raises:
            WorkflowOAuth.ValidationError: If validation fails.
        """
        try:
            return cls(**cls._validate_payload(payload))
        except KeyError as error:
            raise cls.ValidationError(f"Missing required field in workflow OAuth payload: {error.args[0]}") from error
        except Exception as error:
            raise cls.ValidationError(f"Invalid workflow OAuth payload: {error}") from error

    def validate_against_app_info(self, app_info: "B24AppInfoResult") -> bool:
        """
        Validate workflow OAuth data against application info.

        Args:
            app_info: Application info result.

        Returns:
            True if validation succeeds.

        Raises:
            WorkflowOAuth.ValidationError: If validation fails.
        """
        try:
            return super(WorkflowOAuth, self).validate_against_app_info(app_info)
        except self.ValidationError as error:
            raise self.ValidationError("Invalid workflow OAuth") from error
