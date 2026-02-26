from dataclasses import asdict, dataclass
from datetime import datetime
from typing import TYPE_CHECKING, Any, Mapping, Optional, Text

from .._config import Config
from .._constants import PYTHON_VERSION
from ..error import BitrixValidationError
from ..utils.types import JSONDict
from ._utils import parse_flattened_keys
from .auth import EventOAuth

if TYPE_CHECKING:
    from ..api.responses import B24AppInfoResult

__all__ = [
    "OAuthEventData",
]

_DATACLASS_KWARGS = {"eq": False, "frozen": True}

if PYTHON_VERSION >= (3, 10):
    _DATACLASS_KWARGS["slots"] = True


@dataclass(**_DATACLASS_KWARGS)
class OAuthEventData:
    """"""

    class ValidationError(BitrixValidationError):
        """"""

    event: Text
    event_handler_id: int
    ts: datetime
    auth: EventOAuth
    data: Optional[JSONDict] = None

    @classmethod
    def from_dict(cls, payload: Mapping[Text, Any], /) -> "OAuthEventData":
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
        """"""
        return self.auth.is_system

    def validate_against_app_info(self, app_info: "B24AppInfoResult") -> bool:
        """"""
        try:
            return self.auth.validate_against_app_info(app_info)
        except self.auth.ValidationError as error:
            raise self.ValidationError("Invalid oauth event data") from error

    def to_dict(self) -> JSONDict:
        """"""
        return asdict(self)
