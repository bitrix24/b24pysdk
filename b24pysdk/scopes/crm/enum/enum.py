from ....bitrix_api.classes import BitrixAPIRequest
from ....scopes.crm.base_crm import BaseCRM
from ....utils.functional import type_checker
from ....utils.types import Timeout
from .settings import Settings


class Enum(BaseCRM):
    """"""

    @property
    def settings(self) -> Settings:
        """"""
        return Settings(self)

    @type_checker
    def activitydirection(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.activitydirection),
            timeout=timeout,
        )

    @type_checker
    def activitynotifytype(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.activitynotifytype),
            timeout=timeout,
        )

    @type_checker
    def activitypriority(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.activitypriority),
            timeout=timeout,
        )

    @type_checker
    def activitystatus(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.activitystatus),
            timeout=timeout,
        )

    @type_checker
    def activitytype(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.activitytype),
            timeout=timeout,
        )

    @type_checker
    def addresstype(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.addresstype),
            timeout=timeout,
        )

    @type_checker
    def contenttype(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.contenttype),
            timeout=timeout,
        )

    @type_checker
    def getorderownertypes(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.getorderownertypes),
            timeout=timeout,
        )

    @type_checker
    def fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._fields(timeout=timeout)

    @type_checker
    def ownertype(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.ownertype),
            timeout=timeout,
        )
