from typing import Optional, Text

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Check",
]


class Check(BaseEntity):
    """"""

    @type_checker
    def apply(
        self,
        uuid: Text,
        *,
        print_end_time: Optional[Text] = None,
        reg_number_kkt: Optional[Text] = None,
        fiscal_doc_attr: Optional[Text] = None,
        fiscal_doc_number: Optional[Text] = None,
        fiscal_receipt_number: Optional[Text] = None,
        fn_number: Optional[Text] = None,
        shift_number: Optional[Text] = None,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = dict()
        params["UUID"] = uuid

        if print_end_time is not None:
            params["PRINT_END_TIME"] = print_end_time

        if reg_number_kkt is not None:
            params["REG_NUMBER_KKT"] = reg_number_kkt

        if fiscal_doc_attr is not None:
            params["FISCAL_DOC_ATTR"] = fiscal_doc_attr

        if fiscal_doc_number is not None:
            params["FISCAL_DOC_NUMBER"] = fiscal_doc_number

        if fiscal_receipt_number is not None:
            params["FISCAL_RECEIPT_NUMBER"] = fiscal_receipt_number

        if fn_number is not None:
            params["FN_NUMBER"] = fn_number

        if shift_number is not None:
            params["SHIFT_NUMBER"] = shift_number

        return self._make_bitrix_api_request(
            api_wrapper=self.apply,
            params=params,
            timeout=timeout,
        )
