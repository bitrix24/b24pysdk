from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..api.responses import B24AppInfoResult
    from . import AbstractBitrixApp
    from .bitrix_token import BitrixToken


class AppInfoCacheMethods:
    """
    Mixin with common ``app.info`` cache behavior.

    Subclasses must provide ``_make_bitrix_token`` and must define
    ``_app_info`` in ``__slots__``.
    """

    __slots__ = ()

    if TYPE_CHECKING:
        _app_info: "B24AppInfoResult"

    def _set_app_info_cache(self, app_info: "B24AppInfoResult"):
        """Store ``app.info`` result in internal cache."""
        object.__setattr__(self, "_app_info", app_info)

    def _make_bitrix_token(self, bitrix_app: "AbstractBitrixApp") -> "BitrixToken":
        """
        Create a Bitrix token used to call ``app.info``.

        Subclasses must implement this method because token construction
        differs for OAuth payloads and placement data.
        """
        raise NotImplementedError

    def get_app_info(self, bitrix_app: "AbstractBitrixApp") -> "B24AppInfoResult":
        """
        Resolve and cache Bitrix24 ``app.info``.

        Args:
            bitrix_app: SDK application object with client credentials.

        Returns:
            Cached or freshly loaded Bitrix24 application installation info.
        """

        if not hasattr(self, "_app_info"):
            bitrix_token = self._make_bitrix_token(bitrix_app)
            self._set_app_info_cache(bitrix_token.get_app_info().result)

        return self._app_info
