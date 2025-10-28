from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Text
from urllib.parse import urlparse

from ..._constants import PYTHON_VERSION as _PV
from ...constants import B24AppStatus
from ...error import BitrixValidationError
from ...utils.types import JSONDict
from .oauth_token import OAuthToken

_DATACLASS_KWARGS = {"eq": False, "frozen": True}

if _PV >= (3, 10):
    _DATACLASS_KWARGS["slots"] = True


@dataclass(**_DATACLASS_KWARGS)
class RenewedOAuthToken:
    """"""

    class ValidationError(BitrixValidationError):
        """"""

    oauth_token: OAuthToken
    member_id: Text
    client_endpoint: Text
    server_endpoint: Text
    domain: Text
    scope: List[Text]
    status: B24AppStatus
    application_token: Optional[Text] = None

    @classmethod
    def from_dict(cls, renewed_oauth_token_payload: JSONDict) -> "RenewedOAuthToken":
        try:
            return cls(
                oauth_token=OAuthToken.from_dict(renewed_oauth_token_payload),
                member_id=renewed_oauth_token_payload["member_id"],
                client_endpoint=renewed_oauth_token_payload["client_endpoint"],
                server_endpoint=renewed_oauth_token_payload["server_endpoint"],
                domain=renewed_oauth_token_payload["domain"],
                scope=renewed_oauth_token_payload["scope"].split(","),
                status=B24AppStatus(renewed_oauth_token_payload["status"]),
                application_token=renewed_oauth_token_payload.get("application_token"),
            )
        except KeyError as error:
            raise cls.ValidationError(f"Missing required field in renewed OAuth token payload: {error.args[0]}") from error
        except Exception as error:
            raise cls.ValidationError(f"Invalid renewed OAuth token payload: {error}") from error

    @property
    def portal_domain(self) -> Text:
        """"""
        return urlparse(self.client_endpoint).hostname

    def to_dict(self) -> Dict:
        return asdict(self)
