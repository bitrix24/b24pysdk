import json
from dataclasses import asdict, dataclass, field
from typing import TYPE_CHECKING, Any, Mapping, Optional, Text

from .._constants import PYTHON_VERSION
from ..constants import B24AppStatus, Protocol
from ..errors import BitrixValidationError
from ..utils.types import JSONDict
from .bitrix_token import BitrixToken
from .oauth_token import OAuthToken

if TYPE_CHECKING:
    from ..api.responses import B24AppInfoResult
    from .bitrix_app import AbstractBitrixApp

__all__ = [
    "OAuthPlacementData",
]

_DATACLASS_KWARGS = {"eq": False, "frozen": True}

if PYTHON_VERSION >= (3, 10):
    _DATACLASS_KWARGS["slots"] = True


@dataclass(**_DATACLASS_KWARGS)
class OAuthPlacementData:
    """
    Represents OAuth placement data received from Bitrix24.

    Combines OAuth token information with metadata about the application
    installation context (domain, protocol, language, placement, etc.).
    """

    class ValidationError(BitrixValidationError):
        """Raised when placement data validation fails."""

    oauth_token: OAuthToken
    domain: Text
    protocol: Protocol
    lang: Text
    app_sid: Text
    member_id: Text
    status: B24AppStatus
    placement: Optional[Text] = None
    placement_options: Optional[JSONDict] = None

    if TYPE_CHECKING:
        _app_info: "B24AppInfoResult" = field(init=False)

    @classmethod
    def from_dict(cls, payload: Mapping[Text, Any], /) -> "OAuthPlacementData":
        """
        Create an OAuthPlacementData instance from placement payload.

        Args:
            payload: Mapping containing Bitrix24 placement data fields such as
                'DOMAIN', 'PROTOCOL', 'LANG', 'APP_SID', 'member_id',
                'status', 'PLACEMENT', and 'PLACEMENT_OPTIONS'.

        Returns:
            OAuthPlacementData instance.

        Raises:
            OAuthPlacementData.ValidationError: If required fields are missing
                or payload contains invalid values.
        """

        try:
            oauth_token = OAuthToken.from_placement_data(payload)

            domain = payload["DOMAIN"]
            protocol = Protocol(int(payload["PROTOCOL"]))
            lang = payload["LANG"]
            app_sid = payload["APP_SID"]
            member_id = payload["member_id"]
            status = B24AppStatus(payload["status"])
            placement = payload.get("PLACEMENT")
            placement_options = payload.get("PLACEMENT_OPTIONS")

            if placement_options and isinstance(placement_options, str):
                placement_options = json.loads(placement_options)

            return cls(
                oauth_token=oauth_token,
                domain=domain,
                protocol=protocol,
                lang=lang,
                app_sid=app_sid,
                member_id=member_id,
                status=status,
                placement=placement,
                placement_options=placement_options,
            )

        except KeyError as error:
            raise cls.ValidationError(f"Missing required field in placement data: {error.args[0]}") from error

        except Exception as error:
            raise cls.ValidationError(f"Invalid placement data: {error}") from error

    def get_app_info(self, bitrix_app: "AbstractBitrixApp") -> "B24AppInfoResult":
        """
        Resolve and cache Bitrix24 ``app.info`` for this placement launch.

        Args:
            bitrix_app: SDK application object with client credentials. It is
                used together with the placement OAuth token to call
                Bitrix24 ``app.info``.

        Returns:
            Bitrix24 application installation information used to validate that
            the placement launch belongs to the expected application.
        """

        if not hasattr(self, "_app_info"):
            bitrix_token = BitrixToken.from_oauth_placement_data(oauth_placement_data=self, bitrix_app=bitrix_app)
            object.__setattr__(self, "_app_info", bitrix_token.get_app_info().result)

        return self._app_info

    def validate_against_app_info(self, app_info: "B24AppInfoResult") -> bool:
        """
        Validate placement data against application installation info.

        Args:
            app_info: Application info result containing installation metadata.

        Returns:
            True if placement data matches the application installation.

        Raises:
            OAuthPlacementData.ValidationError: If validation fails.
        """
        if all((
                self.member_id == app_info.install.member_id,
                self.domain == app_info.install.domain,
        )):
            return True
        else:
            raise self.ValidationError("Invalid placement data")

    def to_dict(self) -> JSONDict:
        """
        Convert the OAuthPlacementData instance to a dictionary.

        Returns:
            Dictionary representation of the placement data.
        """
        return asdict(self)
