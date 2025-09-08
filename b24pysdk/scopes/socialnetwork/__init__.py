from typing import TYPE_CHECKING

from ..scope import Scope
from .api import API

if TYPE_CHECKING:
    from ... import Client

__all__ = [
    "Socialnetwork",
]


class Socialnetwork(Scope):
    """"""

    def __init__(self, client: "Client"):
        super().__init__(client)
        self.api = API(self)
