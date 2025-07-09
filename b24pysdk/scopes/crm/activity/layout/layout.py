from typing import TYPE_CHECKING

from ...base_crm import BaseCRM
from .blocks import Blocks

if TYPE_CHECKING:
    from ..activity import Activity


class Layout(BaseCRM):
    """"""
    def __init__(self, activity: "Activity"):
        super().__init__(activity._scope)
        self._path = self._get_path(activity)

    @property
    def blocks(self) -> Blocks:
        """"""
        return Blocks(self)
