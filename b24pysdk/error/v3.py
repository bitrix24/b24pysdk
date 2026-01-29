from dataclasses import asdict, dataclass
from functools import cached_property
from typing import Dict, List, Optional, Text

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

    __slots__ = ()

    @cached_property
    def error(self) -> Error:
        """"""
        return Error.from_dict(self.json_response["error"])

    @cached_property
    def code(self) -> Text:
        """"""
        return self.error.code

    @cached_property
    def validation(self) -> Optional[List[Validation]]:
        """"""
        return self.error.validation

    @cached_property
    def has_validation(self) -> bool:
        """"""
        return bool(self.validation)
