from dataclasses import dataclass

from .._constants import PYTHON_VERSION

__all__ = [
    "BaseBitrixEvent",
]

_DATACLASS_KWARGS = {"eq": False, "frozen": True}

if PYTHON_VERSION >= (3, 10):
    _DATACLASS_KWARGS["slots"] = True


@dataclass(**_DATACLASS_KWARGS)
class BaseBitrixEvent:
    """"""
