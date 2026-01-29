from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Text

import requests

from .._constants import PYTHON_VERSION as _PV
from ..utils.types import JSONDict
from . import BaseBitrixAPIError

_DATACLASS_KWARGS = {"eq": False, "frozen": True}

if _PV >= (3, 10):
    _DATACLASS_KWARGS["slots"] = True

__all__ = [
    "BitrixAPIError",
]


@dataclass(**_DATACLASS_KWARGS)
class Validation:
    field: Text
    message: Text

    @classmethod
    def from_dict(cls, json_response: JSONDict) -> "Validation":
        return cls(
            field=json_response["field"],
            message=json_response["message"],
        )

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass(**_DATACLASS_KWARGS)
class Error:
    code: Text
    message: Text
    validation: Optional[List[Validation]]

    @classmethod
    def from_dict(cls, json_response: JSONDict) -> "Error":
        validation = json_response.get("validation")

        if isinstance(validation, list):
            validation = [Validation.from_dict(item) for item in validation]

        return cls(
            code=json_response["code"],
            message=json_response["message"],
            validation=validation,
        )

    def to_dict(self) -> Dict:
        return asdict(self)


class BitrixAPIError(BaseBitrixAPIError):
    """Bitrix v3 API error"""

    __slots__ = ("error",)

    error: Error

    def __init__(self, json_response: JSONDict, response: requests.Response):
        super().__init__(json_response, response)
        self.error = Error.from_dict(json_response["error"])

    @property
    def code(self) -> Text:
        return self.error.code

    @property
    def validation(self) -> Optional[List[Validation]]:
        return self.error.validation

    @property
    def has_validation(self) -> bool:
        return bool(self.validation)
