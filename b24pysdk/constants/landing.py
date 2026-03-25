from ..utils import enum as _enum

__all__ = [
    "LandingDemoType",
]


class LandingDemoType(_enum.StrEnum):
    """Template types for landing.demos.getSiteList/getPageList type."""
    PAGE = "page"
    STORE = "store"
