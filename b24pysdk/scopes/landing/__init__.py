from functools import cached_property

from .._base_scope import BaseScope
from .block import Block
from .demos import Demos
from .landing import Landing as LandingEntity
from .repo import Repo
from .repowidget import RepoWidget
from .role import Role
from .site import Site
from .syspage import SysPage
from .template import Template

__all__ = [
    "Landing",
]


class Landing(BaseScope):
    """"""

    @cached_property
    def block(self) -> Block:
        """"""
        return Block(self)

    @cached_property
    def landing(self) -> LandingEntity:
        """"""
        return LandingEntity(self)

    @cached_property
    def site(self) -> Site:
        """"""
        return Site(self)

    @cached_property
    def role(self) -> Role:
        """"""
        return Role(self)

    @cached_property
    def repo(self) -> Repo:
        """"""
        return Repo(self)

    @cached_property
    def template(self) -> Template:
        """"""
        return Template(self)

    @cached_property
    def syspage(self) -> SysPage:
        """"""
        return SysPage(self)

    @cached_property
    def demos(self) -> Demos:
        """"""
        return Demos(self)

    @cached_property
    def repowidget(self) -> RepoWidget:
        """"""
        return RepoWidget(self)
