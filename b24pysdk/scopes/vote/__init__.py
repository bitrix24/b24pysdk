from functools import cached_property

from .._base_scope import BaseScope
from .attached_vote import AttachedVote
from .integration import Integration

__all__ = [
    "Vote",
]


class Vote(BaseScope):
    """"""

    @cached_property
    def attached_vote(self) -> AttachedVote:
        """"""
        return AttachedVote(self)

    @cached_property
    def integration(self) -> Integration:
        """"""
        return Integration(self)
