from dataclasses import dataclass
from typing import Text

from ..._constants import PYTHON_VERSION as _PV
from .base_bitrix_event import BaseBitrixEvent

_DATACLASS_KWARGS = {"eq": False, "frozen": True}

if _PV >= (3, 10):
    _DATACLASS_KWARGS["slots"] = True


@dataclass(**_DATACLASS_KWARGS)
class PortalDomainChangedEvent(BaseBitrixEvent):
    """"""
    old_domain: Text
    new_domain: Text
