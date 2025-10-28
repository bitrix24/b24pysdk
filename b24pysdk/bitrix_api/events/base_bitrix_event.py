from dataclasses import dataclass

from ..._constants import PYTHON_VERSION as _PV

_DATACLASS_KWARGS = {"eq": False, "frozen": True}

if _PV >= (3, 10):
    _DATACLASS_KWARGS["slots"] = True


@dataclass(**_DATACLASS_KWARGS)
class BaseBitrixEvent:
    """"""
