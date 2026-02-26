from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from typing import Any, Mapping, Optional, Text

from .._config import Config
from .._constants import PYTHON_VERSION
from ..error import BitrixValidationError
from ..utils.types import JSONDict

__all__ = [
    "OAuthToken",
]

_DATACLASS_KWARGS = {"eq": False, "frozen": True}

if PYTHON_VERSION >= (3, 10):
    _DATACLASS_KWARGS["slots"] = True


@dataclass(**_DATACLASS_KWARGS)
class OAuthToken:
    """"""

    class ValidationError(BitrixValidationError):
        """"""

    access_token: Text
    refresh_token: Optional[Text]
    expires: Optional[datetime] = None
    expires_in: Optional[int] = None

    @classmethod
    def from_dict(cls, payload: Mapping[Text, Any], /) -> "OAuthToken":
        """"""
        try:
            return cls(
                access_token=payload["access_token"],
                refresh_token=payload.get("refresh_token"),
                expires=datetime.fromtimestamp(int(payload["expires"]), tz=Config().tz),
                expires_in=int(payload["expires_in"]),
            )
        except KeyError as error:
            raise cls.ValidationError(f"Missing required field in OAuth token payload: {error.args[0]}") from error
        except Exception as error:
            raise cls.ValidationError(f"Invalid OAuth token payload: {error}") from error

    @classmethod
    def from_placement_data(cls, payload: Mapping[Text, Any], /) -> "OAuthToken":
        """"""

        try:
            access_token = payload["AUTH_ID"]
            refresh_token = payload["REFRESH_ID"]
            expires_in = int(payload["AUTH_EXPIRES"])
            expires = Config().get_local_datetime() + timedelta(seconds=expires_in)

            return cls(
                access_token=access_token,
                refresh_token=refresh_token,
                expires=expires,
                expires_in=expires_in,
            )

        except KeyError as error:
            raise cls.ValidationError(f"Missing required field in OAuth token placement data: {error.args[0]}") from error

        except Exception as error:
            raise cls.ValidationError(f"Invalid OAuth token placement data: {error}") from error

    @property
    def is_one_off(self) -> bool:
        """"""
        return self.refresh_token is None

    @property
    def has_expired(self) -> Optional[bool]:
        """"""
        return self.expires and self.expires <= Config().get_local_datetime()

    def to_dict(self) -> JSONDict:
        """"""
        return asdict(self)
