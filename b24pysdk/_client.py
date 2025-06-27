from typing import Sequence

from ._bitrix_api_request import BitrixAPIRequest
from .bitrix_api import BitrixToken

from . import scopes


class Client:
    """"""

    __slots__ = ("bitrix_token", "crm")

    bitrix_token: BitrixToken
    crm: scopes.CRM

    def __init__(self, bitrix_token: BitrixToken):
        self.bitrix_token = bitrix_token
        self.crm = scopes.CRM(self)

    def call_batch(self, bitrix_api_requests: Sequence[BitrixAPIRequest]):
        """"""

    def call_batches(self, bitrix_api_requests: Sequence[BitrixAPIRequest]):
        """"""
