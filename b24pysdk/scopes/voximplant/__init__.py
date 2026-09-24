from functools import cached_property

from .._base_scope import BaseScope
from .callback import Callback
from .infocall import Infocall
from .line import Line
from .sip import Sip
from .statistic import Statistic
from .tts import Tts
from .url import Url
from .user import User

__all__ = [
    "Voximplant",
]


class Voximplant(BaseScope):
    """"""

    @cached_property
    def callback(self) -> Callback:
        """"""
        return Callback(self)

    @cached_property
    def infocall(self) -> Infocall:
        """"""
        return Infocall(self)

    @cached_property
    def line(self) -> Line:
        """"""
        return Line(self)

    @cached_property
    def sip(self) -> Sip:
        """"""
        return Sip(self)

    @cached_property
    def statistic(self) -> Statistic:
        """"""
        return Statistic(self)

    @cached_property
    def tts(self) -> Tts:
        """"""
        return Tts(self)

    @cached_property
    def url(self) -> Url:
        """"""
        return Url(self)

    @cached_property
    def user(self) -> User:
        """"""
        return User(self)
