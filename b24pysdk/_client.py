from typing import TYPE_CHECKING, Mapping, Sequence, Union, overload

from . import scopes
from .bitrix_api.protocols import BitrixTokenFullProtocol
from .bitrix_api.requests import BitrixAPIBatchesRequest, BitrixAPIBatchRequest
from .utils.types import JSONDict, Key, Timeout

if TYPE_CHECKING:
    from .bitrix_api.requests import BitrixAPIRequest


class Client:
    """"""

    __slots__ = (
        "_bitrix_token",
        "_kwargs",
        "access",
        "app",
        "calendar",
        "crm",
        "department",
        "disk",
        "entity",
        "event",
        "events",
        "feature",
        "method",
        "placement",
        "profile",
        "scope",
        "server",
        "socialnetwork",
        "user",
    )

    _bitrix_token: BitrixTokenFullProtocol
    _kwargs: JSONDict
    access: scopes.Access
    app: scopes.App
    calendar: scopes.Calendar
    crm: scopes.CRM
    department: scopes.Department
    disk: scopes.Disk
    entity: scopes.Entity
    event: scopes.Event
    events: scopes.Events
    feature: scopes.Feature
    method: scopes.Method
    placement: scopes.Placement
    profile: scopes.Profile
    scope: scopes.Scope
    server: scopes.Server
    socialnetwork: scopes.Socialnetwork
    user: scopes.User

    def __init__(
            self,
            bitrix_token: BitrixTokenFullProtocol,
            *,
            timeout: Timeout = None,
            **kwargs,
    ):
        self._bitrix_token = bitrix_token

        self.access = scopes.Access(self)
        self.app = scopes.App(self)
        self.calendar = scopes.Calendar(self)
        self.crm = scopes.CRM(self)
        self.department = scopes.Department(self)
        self.disk = scopes.Disk(self)
        self.entity = scopes.Entity(self)
        self.event = scopes.Event(self)
        self.events = scopes.Events(self)
        self.feature = scopes.Feature(self)
        self.method = scopes.Method(self)
        self.placement = scopes.Placement(self)
        self.profile = scopes.Profile(self)
        self.scope = scopes.Scope(self)
        self.server = scopes.Server(self)
        self.socialnetwork = scopes.Socialnetwork(self)
        self.user = scopes.User(self)

        self._kwargs = kwargs

        if timeout:
            self._kwargs["timeout"] = timeout

    def __str__(self):
        return f"<Client of portal {self._bitrix_token.domain}>"

    def __repr__(self):
        return f"{self.__class__.__name__}(bitrix_token={self._bitrix_token})"

    @overload
    def call_batch(
            self,
            bitrix_api_requests: Mapping[Key, "BitrixAPIRequest"],
            halt: bool = False,
            ignore_size_limit: bool = False,
            timeout: Timeout = None,
    ) -> BitrixAPIBatchRequest: ...

    @overload
    def call_batch(
            self,
            bitrix_api_requests: Sequence["BitrixAPIRequest"],
            halt: bool = False,
            ignore_size_limit: bool = False,
            timeout: Timeout = None,
    ) -> BitrixAPIBatchRequest: ...

    def call_batch(
            self,
            bitrix_api_requests: Union[Mapping[Key, "BitrixAPIRequest"], Sequence["BitrixAPIRequest"]],
            halt: bool = False,
            ignore_size_limit: bool = False,
            timeout: Timeout = None,
    ) -> BitrixAPIBatchRequest:
        """"""
        return BitrixAPIBatchRequest(
            bitrix_token=self._bitrix_token,
            bitrix_api_requests=bitrix_api_requests,
            halt=halt,
            ignore_size_limit=ignore_size_limit,
            timeout=timeout,
            **self._kwargs,
        )

    @overload
    def call_batches(
            self,
            bitrix_api_requests: Mapping[Key, "BitrixAPIRequest"],
            halt: bool = False,
            timeout: Timeout = None,
    ) -> BitrixAPIBatchRequest: ...

    @overload
    def call_batches(
            self,
            bitrix_api_requests: Sequence["BitrixAPIRequest"],
            halt: bool = False,
            timeout: Timeout = None,
    ) -> BitrixAPIBatchRequest: ...

    def call_batches(
            self,
            bitrix_api_requests: Union[Mapping[Key, "BitrixAPIRequest"], Sequence["BitrixAPIRequest"]],
            halt: bool = False,
            timeout: Timeout = None,
    ) -> BitrixAPIBatchesRequest:
        """"""
        return BitrixAPIBatchesRequest(
            bitrix_token=self._bitrix_token,
            bitrix_api_requests=bitrix_api_requests,
            halt=halt,
            timeout=timeout,
            **self._kwargs,
        )
