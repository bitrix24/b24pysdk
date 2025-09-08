from ..base import Base
from .workgroup import Workgroup


class API(Base):
    """"""

    @property
    def workgroup(self) -> Workgroup:
        """"""
        return Workgroup(self)
