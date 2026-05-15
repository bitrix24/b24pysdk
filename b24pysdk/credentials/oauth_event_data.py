from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING, Any, Mapping, Optional, Text

from .._config import Config
from .._constants import PYTHON_VERSION
from ..errors import BitrixValidationError
from ..utils.types import JSONDict
from ._utils import parse_flattened_keys
from .auth import EventOAuth

if TYPE_CHECKING:
    from ..api.responses import B24AppInfoResult
    from .bitrix_app import AbstractBitrixApp

__all__ = [
    "OAuthEventData",
]

_DATACLASS_KWARGS = {"eq": False, "frozen": True}

if PYTHON_VERSION >= (3, 10):
    _DATACLASS_KWARGS["slots"] = True


@dataclass(**_DATACLASS_KWARGS)
class OAuthEventData:
    """
    Bitrix24 event callback payload with parsed auth data.

    The model accepts both user-context events with OAuth token data and system
    events where OAuth token fields are absent.
    """

    class ValidationError(BitrixValidationError):
        """Raised when event callback payload validation fails."""

    event: Text
    event_handler_id: int
    ts: datetime
    auth: EventOAuth
    data: Optional[JSONDict] = None

    if TYPE_CHECKING:
        _app_info: "B24AppInfoResult" = field(init=False)

    @classmethod
    def from_dict(cls, payload: Mapping[Text, Any], /) -> "OAuthEventData":
        """
        Create an event payload model from raw Bitrix24 request parameters.

        Args:
            payload: Raw event callback parameters. Flattened keys such as
                ``auth[member_id]`` are accepted and normalized internally.

        Returns:
            Parsed event callback payload.
        """
        try:
            parsed_payload = parse_flattened_keys(payload)

            event = parsed_payload["event"]
            event_handler_id = int(parsed_payload["event_handler_id"])
            ts = datetime.fromtimestamp(int(parsed_payload["ts"]), tz=Config().tz)
            auth = EventOAuth.from_dict(parsed_payload["auth"])
            data = parsed_payload.get("data")

            return cls(
                event=event,
                event_handler_id=event_handler_id,
                ts=ts,
                auth=auth,
                data=data,
            )

        except KeyError as error:
            raise cls.ValidationError(f"Missing required field in event data: {error.args[0]}") from error

        except Exception as error:
            raise cls.ValidationError(f"Invalid event data: {error}") from error

    @property
    def is_system(self) -> bool:
        """Whether the event has no user OAuth token and cannot call ``app.info``."""
        return self.auth.is_system

    def get_app_info(self, bitrix_app: "AbstractBitrixApp") -> "B24AppInfoResult":
        """
        Resolve Bitrix24 ``app.info`` through the event auth payload.

        Args:
            bitrix_app: SDK application object used to call ``app.info``.
                Required when integrations validate that the event belongs to
                the expected application.

        Returns:
            Bitrix24 application installation information.
        """
        return self.auth.get_app_info(bitrix_app)

    def validate_against_app_info(self, app_info: "B24AppInfoResult") -> bool:
        """
        Validate event auth data against Bitrix24 ``app.info`` result.

        Args:
            app_info: Application installation information returned by
                ``app.info``.
        """
        try:
            return self.auth.validate_against_app_info(app_info)
        except self.auth.ValidationError as error:
            raise self.ValidationError("Invalid oauth event data") from error

    def to_dict(self) -> JSONDict:
        """Convert the event payload to a dictionary."""
        return asdict(self)
