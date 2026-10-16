from typing import Optional, Text

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Check",
]


class Check(BaseEntity):
    """Class for saving receipt printing result.

    Documentation: https://apidocs.bitrix24.com/api-reference/sale/cashbox/index.html
    """

    @type_checker
    def apply(
        self,
        uuid: Text,
        *,
        print_end_time: Optional[Text] = MISSING,
        reg_number_kkt: Optional[Text] = MISSING,
        fiscal_doc_attr: Optional[Text] = MISSING,
        fiscal_doc_number: Optional[Text] = MISSING,
        fiscal_receipt_number: Optional[Text] = MISSING,
        fn_number: Optional[Text] = MISSING,
        shift_number: Optional[Text] = MISSING,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Save the result of printing the receipt

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/cashbox/sale-cashbox-check-apply.html

        The method saves the result of printing a receipt that was printed on REST cash register.

        Args:
            uuid: UUID of the receipt;

            print_end_time: Time when the receipt printing ended;

            reg_number_kkt: Registration number of the cash register;

            fiscal_doc_attr: Fiscal attribute of the document;

            fiscal_doc_number: Fiscal document number;

            fiscal_receipt_number: Fiscal receipt number;

            fn_number: Fiscal storage number;

            shift_number: Shift number;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "UUID": uuid,
        }

        if print_end_time is not MISSING:
            params["PRINT_END_TIME"] = print_end_time

        if reg_number_kkt is not MISSING:
            params["REG_NUMBER_KKT"] = reg_number_kkt

        if fiscal_doc_attr is not MISSING:
            params["FISCAL_DOC_ATTR"] = fiscal_doc_attr

        if fiscal_doc_number is not MISSING:
            params["FISCAL_DOC_NUMBER"] = fiscal_doc_number

        if fiscal_receipt_number is not MISSING:
            params["FISCAL_RECEIPT_NUMBER"] = fiscal_receipt_number

        if fn_number is not MISSING:
            params["FN_NUMBER"] = fn_number

        if shift_number is not MISSING:
            params["SHIFT_NUMBER"] = shift_number

        return self._make_bitrix_api_request(
            api_wrapper=self.apply,
            params=params,
            timeout=timeout,
        )
