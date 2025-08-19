from abc import ABC, abstractmethod
from typing import Text


class AbstractBitrixApp(ABC):
    """"""

    client_id: Text = NotImplemented
    """"""

    client_secret: Text = NotImplemented
    """"""

    @abstractmethod
    def __init__(self, *args, **kwargs):
        """"""
        super().__init__(*args, **kwargs)


class BitrixApp(AbstractBitrixApp):
    """Local or market bitrix application"""

    def __init__(
            self,
            client_id: Text,
            client_secret: Text,
    ):
        self.client_id = client_id
        self.client_secret = client_secret


class LocalBitrixApp(BitrixApp):
    """"""

    domain: Text
    """"""

    def __init__(
            self,
            domain: Text,
            client_id: Text,
            client_secret: Text,
    ):
        super().__init__(client_id, client_secret)
        self.domian = domain
