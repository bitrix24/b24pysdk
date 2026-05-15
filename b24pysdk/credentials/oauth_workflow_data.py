from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Mapping, Optional, Text

from .._config import Config
from .._constants import PYTHON_VERSION
from ..constants import B24BoolLit
from ..errors import BitrixValidationError
from ..utils.types import JSONDict
from ._utils import parse_flattened_keys
from .auth import WorkflowOAuth

if TYPE_CHECKING:
    from ..api.responses import B24AppInfoResult
    from .bitrix_app import AbstractBitrixApp

__all__ = [
    "OAuthWorkflowData",
]

_DATACLASS_KWARGS = {"eq": False, "frozen": True}

if PYTHON_VERSION >= (3, 10):
    _DATACLASS_KWARGS["slots"] = True


@dataclass(**_DATACLASS_KWARGS)
class OAuthWorkflowData:
    """Bitrix24 workflow robot callback payload with parsed auth data."""

    class ValidationError(BitrixValidationError):
        """Raised when workflow callback payload validation fails."""

    workflow_id: Text
    code: Text
    document_id: List[Text]
    document_type: List[Text]
    event_token: Text
    use_subscription: bool
    timeout_duration: int
    ts: datetime
    auth: WorkflowOAuth
    properties: Optional[JSONDict] = None

    if TYPE_CHECKING:
        _app_info: "B24AppInfoResult" = field(init=False)

    @classmethod
    def from_dict(cls, workflow_data: Mapping[Text, Any]) -> "OAuthWorkflowData":
        """
        Create a workflow payload model from raw Bitrix24 request parameters.

        Args:
            workflow_data: Raw workflow robot callback parameters. Flattened
                keys such as ``auth[member_id]`` are accepted and normalized
                internally.

        Returns:
            Parsed workflow robot payload.
        """
        try:
            parsed_workflow_data = parse_flattened_keys(workflow_data)

            workflow_id = parsed_workflow_data["workflow_id"]
            code = parsed_workflow_data["code"]
            document_id = parsed_workflow_data["document_id"]
            document_type = parsed_workflow_data["document_type"]
            event_token = parsed_workflow_data["event_token"]
            use_subscription = bool(B24BoolLit(parsed_workflow_data["use_subscription"]))
            timeout_duration = int(parsed_workflow_data["timeout_duration"])
            ts = datetime.fromtimestamp(int(parsed_workflow_data["ts"]), tz=Config().tz)
            auth = WorkflowOAuth.from_dict(parsed_workflow_data["auth"])
            properties = parsed_workflow_data.get("properties")

            return cls(
                workflow_id=workflow_id,
                code=code,
                document_id=document_id,
                document_type=document_type,
                event_token=event_token,
                use_subscription=use_subscription,
                timeout_duration=timeout_duration,
                ts=ts,
                auth=auth,
                properties=properties,
            )

        except KeyError as error:
            raise cls.ValidationError(f"Missing required field in workflow data: {error.args[0]}") from error

        except Exception as error:
            raise cls.ValidationError(f"Invalid workflow data: {error}") from error

    def get_app_info(self, bitrix_app: "AbstractBitrixApp") -> "B24AppInfoResult":
        """
        Resolve Bitrix24 ``app.info`` through the workflow auth payload.

        Args:
            bitrix_app: SDK application object used to call ``app.info``.
                Required when integrations validate that the workflow callback
                belongs to the expected application.

        Returns:
            Bitrix24 application installation information.
        """
        return self.auth.get_app_info(bitrix_app)

    def validate_against_app_info(self, app_info: "B24AppInfoResult") -> bool:
        """
        Validate workflow auth data against Bitrix24 ``app.info`` result.

        Args:
            app_info: Application installation information returned by
                ``app.info``.
        """
        try:
            return self.auth.validate_against_app_info(app_info)
        except self.auth.ValidationError as error:
            raise self.ValidationError("Invalid oauth workflow data") from error

    def to_dict(self) -> JSONDict:
        """Convert the workflow payload to a dictionary."""
        return asdict(self)
