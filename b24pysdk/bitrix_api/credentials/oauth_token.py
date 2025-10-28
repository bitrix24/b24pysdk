from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from typing import Dict, Optional, Text

from ..._constants import PYTHON_VERSION as _PV
from ...error import BitrixValidationError
from ...utils.types import JSONDict

_DATACLASS_KWARGS = {"eq": False, "frozen": True}

if _PV >= (3, 10):
    _DATACLASS_KWARGS["slots"] = True


@dataclass(**_DATACLASS_KWARGS)
class OAuthToken:
    """"""

    class ValidationError(BitrixValidationError):
        """"""

    access_token: Text
    refresh_token: Optional[Text]
    expires: Optional[datetime]
    expires_in: Optional[int] = None

    @classmethod
    def from_dict(cls, oauth_token_payload: JSONDict) -> "OAuthToken":
        """"""
        try:
            return cls(
                access_token=oauth_token_payload["access_token"],
                refresh_token=oauth_token_payload["refresh_token"],
                expires=datetime.fromtimestamp(int(oauth_token_payload["expires"])).astimezone(),
                expires_in=int(oauth_token_payload["expires_in"]),
            )
        except KeyError as error:
            raise cls.ValidationError(f"Missing required field in OAuth token payload: {error.args[0]}") from error
        except Exception as error:
            raise cls.ValidationError(f"Invalid OAuth token payload: {error}") from error

    @classmethod
    def from_placement_data(cls, placement_data: JSONDict) -> "OAuthToken":
        """"""

        try:
            access_token = placement_data["AUTH_ID"]
            refresh_token = placement_data["REFRESH_ID"]
            expires_in = int(placement_data["AUTH_EXPIRES"])
            expires = datetime.now().astimezone() + timedelta(seconds=expires_in)

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
        return bool(self.refresh_token)

    @property
    def has_expired(self) -> Optional[bool]:
        """"""
        return self.expires and self.expires <= datetime.now().astimezone()

    def to_dict(self) -> Dict:
        return asdict(self)
