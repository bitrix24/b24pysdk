from ..item.details import Details as BaseDetails
from .configuration import Configuration


class Details(BaseDetails):
    """"""

    @property
    def configuration(self) -> Configuration:
        """"""
        return Configuration(self)
