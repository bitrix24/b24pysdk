from typing import Optional, TYPE_CHECKING

from ....._bitrix_api_request import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict

from ...base_crm import BaseCRM

if TYPE_CHECKING:
    from .payment import Payment


class Product(BaseCRM):
    """"""

    def __init__(self, payment: "Payment"):
        super().__init__(payment._scope)
        self._path = self._get_path(payment)

    @type_checker
    def add(
            self,
            *,
            payment_id: int,
            row_id: int,
            quantity: float,
            timeout: Optional[int] = None
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "paymentId": payment_id,
            "rowId": row_id,
            "quantity": quantity,
        }

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.add),
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            *,
            payment_id: int,
            filter: JSONDict,
            order: Optional[JSONDict] = None,
            timeout: Optional[int] = None
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "paymentId": payment_id,
            "filter": filter
        }

        if order is not None:
            params["order"] = order

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.list),
            params=params,
            timeout=timeout,
        )

    def delete(
            self,
            bitrix_id: int,
            *,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """"""
        return super().delete(bitrix_id, timeout=timeout)

    @type_checker
    def set_quantity(
            self,
            bitrix_id: int,
            *,
            quantity: float,
            timeout: Optional[int] = None
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "id": bitrix_id,
            "quantity": quantity,
        }

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.set_quantity),
            params=params,
            timeout=timeout,
        )
