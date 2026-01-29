import inspect
from abc import ABC
from typing import TYPE_CHECKING, ClassVar, List, Literal, Mapping, Optional, Sequence, Text, Union, overload

from . import scopes
from .bitrix_api.requests import BitrixAPIBatchesRequest, BitrixAPIBatchRequest
from .constants.version import B24APIVersion
from .protocols import BitrixTokenFullProtocol
from .scopes import v3 as scopes_v3

# noinspection PyProtectedMember
from .scopes._base_context import BaseContext
from .utils.types import B24APIVersionLiteral, JSONDict, Key, Timeout

if TYPE_CHECKING:
    from .bitrix_api.requests import AbstractBitrixAPIRequest

__all__ = [
    "BaseClient",
    "Client",
    "ClientV1",
    "ClientV2",
    "ClientV3",
]


class BaseClient(ABC):
    """"""

    VERSION: ClassVar[B24APIVersionLiteral]

    __slots__ = (
        "_bitrix_token",
        "_kwargs",
        "access",
        "app",
        "biconnector",
        "bizproc",
        "calendar",
        "crm",
        "department",
        "disk",
        "documentation",
        "entity",
        "event",
        "events",
        "feature",
        "method",
        "placement",
        "profile",
        "sale",
        "scope",
        "server",
        "socialnetwork",
        "tasks",
        "user",
    )

    _bitrix_token: BitrixTokenFullProtocol
    _kwargs: JSONDict

    access: scopes.Access
    app: scopes.App
    biconnector: scopes.Biconnector
    bizproc: scopes.Bizproc
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
    sale: scopes.Sale
    scope: scopes.Scope
    server: scopes.Server
    socialnetwork: scopes.Socialnetwork
    user: scopes.User

    def __init__(
            self,
            bitrix_token: BitrixTokenFullProtocol,
            *,
            timeout: Timeout = None,
            max_retries: Optional[int] = None,
            initial_retry_delay: Optional[float] = None,
            retry_delay_increment: Optional[float] = None,
            **kwargs,
    ):
        self._bitrix_token = bitrix_token

        self.access = scopes.Access(self)
        self.app = scopes.App(self)
        self.biconnector = scopes.Biconnector(self)
        self.bizproc = scopes.Bizproc(self)
        self.calendar = scopes.Calendar(self)
        self.documentation = scopes_v3.Documentation(self)
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
        self.sale = scopes.Sale(self)
        self.scope = scopes.Scope(self)
        self.server = scopes.Server(self)
        self.socialnetwork = scopes.Socialnetwork(self)
        self.user = scopes.User(self)

        self._kwargs = kwargs
        self._kwargs["prefer_version"] = self.VERSION

        if timeout is not None:
            self._kwargs["timeout"] = timeout

        if max_retries is not None:
            self._kwargs["max_retries"] = max_retries

        if initial_retry_delay is not None:
            self._kwargs["initial_retry_delay"] = initial_retry_delay\

        if retry_delay_increment is not None:
            self._kwargs["retry_delay_increment"] = retry_delay_increment

    def __str__(self):
        if hasattr(self._bitrix_token, "domain"):
            return f"<{self.__class__.__name__} of portal {self._bitrix_token.domain}>"
        else:
            return repr(self)

    def __repr__(self):
        return f"{self.__class__.__name__}(bitrix_token={self._bitrix_token})"

    @overload
    def call_batch(
            self,
            bitrix_api_requests: Mapping[Key, "AbstractBitrixAPIRequest"],
            *,
            halt: bool = False,
            ignore_size_limit: bool = False,
            timeout: Timeout = None,
            **kwargs,
    ) -> BitrixAPIBatchRequest[Mapping[Key, "AbstractBitrixAPIRequest"]]: ...

    @overload
    def call_batch(
            self,
            bitrix_api_requests: Sequence["AbstractBitrixAPIRequest"],
            *,
            halt: bool = False,
            ignore_size_limit: bool = False,
            timeout: Timeout = None,
            **kwargs,
    ) -> BitrixAPIBatchRequest[Sequence["AbstractBitrixAPIRequest"]]: ...

    def call_batch(
            self,
            bitrix_api_requests: Union[Mapping[Key, "AbstractBitrixAPIRequest"], Sequence["AbstractBitrixAPIRequest"]],
            *,
            halt: bool = False,
            ignore_size_limit: bool = False,
            timeout: Timeout = None,
            **kwargs,
    ) -> BitrixAPIBatchRequest:
        """
        Execute multiple API requests in a single batch call.

        Args:
            bitrix_api_requests: Collection of BitrixAPIRequest objects to execute.
            halt: If True, stops processing on first error. Returns results up to that point.
            ignore_size_limit: Ignore batch size limitations if True.
            timeout: Timeout for the batch request in seconds.

        Returns:
            BitrixAPIBatchRequest instance for executing the batch.
        """

        kwargs = self._kwargs | kwargs

        if timeout is not None:
            kwargs["timeout"] = timeout

        return BitrixAPIBatchRequest(
            bitrix_token=self._bitrix_token,
            bitrix_api_requests=bitrix_api_requests,
            halt=halt,
            ignore_size_limit=ignore_size_limit,
            **kwargs,
        )

    @overload
    def call_batches(
            self,
            bitrix_api_requests: Mapping[Key, "AbstractBitrixAPIRequest"],
            *,
            halt: bool = False,
            timeout: Timeout = None,
            **kwargs,
    ) -> BitrixAPIBatchRequest[Mapping[Key, "AbstractBitrixAPIRequest"]]: ...

    @overload
    def call_batches(
            self,
            bitrix_api_requests: Sequence["AbstractBitrixAPIRequest"],
            *,
            halt: bool = False,
            timeout: Timeout = None,
            **kwargs,
    ) -> BitrixAPIBatchRequest[Sequence["AbstractBitrixAPIRequest"]]: ...

    def call_batches(
            self,
            bitrix_api_requests: Union[Mapping[Key, "AbstractBitrixAPIRequest"], Sequence["AbstractBitrixAPIRequest"]],
            halt: bool = False,
            timeout: Timeout = None,
            **kwargs,
    ) -> BitrixAPIBatchesRequest:
        """
        Execute multiple API requests in parallel batches.

        Args:
            bitrix_api_requests: Collection of BitrixAPIRequest objects to execute.
            halt: If True, stops processing on first error. Returns results up to that point.
            timeout: Timeout for the batches request in seconds.

        Returns:
            BitrixAPIBatchesRequest instance for executing parallel batches.
        """

        kwargs = self._kwargs | kwargs

        if timeout is not None:
            kwargs["timeout"] = timeout

        return BitrixAPIBatchesRequest(
            bitrix_token=self._bitrix_token,
            bitrix_api_requests=bitrix_api_requests,
            halt=halt,
            **kwargs,
        )

    def __get_context_by_path(self, path: Text) -> BaseContext:
        """Retrieve a context object by its dot-separated path."""

        if not path:
            raise ValueError("Path cannot be empty")

        try:
            context = self

            for part in path.split("."):
                context = getattr(context, part)

        except AttributeError as error:
            raise ValueError(f"Path {path!r} not found: {error}") from error

        else:
            if not isinstance(context, BaseContext):
                raise TypeError(
                    f"Path {path!r} points to an object of type {type(context).__name__!r}, "
                    f"which is not a BaseContext descendant",
                )

            return context

    def __collect_api_methods(self, context: Union[BaseContext, "BaseClient"]) -> List[Text]:
        """Collect all available API methods from a context."""

        api_methods: List[Text] = []

        for attr_name, value in inspect.getmembers(context):
            if attr_name == "__call__":
                api_methods.append(str(context))

            elif attr_name.startswith("_"):
                continue

            elif isinstance(value, BaseContext):
                api_methods.extend(self.__collect_api_methods(value))

            elif not isinstance(context, self.__class__):
                api_methods.append(f"{context}.{attr_name}")

        return api_methods

    def get_supported_api_methods(self, context: Optional[Union[BaseContext, Text]] = None) -> List[Text]:
        """
        Get a list of all supported API methods.

        Args:
            context: Optional context object or path to filter methods.
                     If None, returns all available methods.

        Returns:
            Sorted list of available API method names.
        """

        if context is None:
            context_object = self

        elif isinstance(context, BaseContext):
            context_object = context

        elif isinstance(context, str):
            context_object = self.__get_context_by_path(context)

        else:
            raise TypeError(
                f"Invalid argument type {type(context).__name__!r}. "
                f"The method accepts only 'str' (API path), 'None', or an instance of BaseContext.",
            )

        return sorted(self.__collect_api_methods(context_object))

    def print_supported_api_methods(self, context: Optional[Union[BaseContext, Text]] = None):
        """
        Print all supported API methods to console.

        Args:
            context: Optional context object or path to filter methods.
                     If None, prints all available methods.
        """

        supported_api_methods = self.get_supported_api_methods(context)

        print("\n".join(supported_api_methods))
        print(f"\nTotal supported api methods: {len(supported_api_methods)}")


class ClientV1(BaseClient):
    """"""

    VERSION: ClassVar[B24APIVersionLiteral] = B24APIVersion.V1

    __slots__ = ()


class ClientV2(ClientV1):
    """"""

    VERSION: ClassVar[B24APIVersionLiteral] = B24APIVersion.V2

    __slots__ = ()


class ClientV3(BaseClient):
    """"""

    VERSION: ClassVar[B24APIVersionLiteral] = B24APIVersion.V3

    __slots__ = (
        "documentation",
        "main",
        "rest",
        "tasks",
    )

    documentation: scopes_v3.Documentation
    main: scopes_v3.Main
    rest: scopes_v3.Rest
    tasks: scopes_v3.Tasks

    def __init__(
            self,
            bitrix_token: BitrixTokenFullProtocol,
            *,
            timeout: Timeout = None,
            max_retries: Optional[int] = None,
            initial_retry_delay: Optional[float] = None,
            retry_delay_increment: Optional[float] = None,
            **kwargs,
    ):
        super().__init__(
            bitrix_token,
            timeout=timeout,
            max_retries=max_retries,
            initial_retry_delay=initial_retry_delay,
            retry_delay_increment=retry_delay_increment,
            **kwargs,
        )
        self.documentation = scopes_v3.Documentation(self)
        self.main = scopes_v3.Main(self)
        self.rest = scopes_v3.Rest(self)
        self.tasks = scopes_v3.Tasks(self)


# noinspection PyPep8Naming
@overload
def Client(
        bitrix_token: BitrixTokenFullProtocol,
        *,
        prefer_version: Literal[2] = B24APIVersion.V2,
        timeout: Timeout = None,
        max_retries: Optional[int] = None,
        initial_retry_delay: Optional[float] = None,
        retry_delay_increment: Optional[float] = None,
        **kwargs,
) -> ClientV2: ...


# noinspection PyPep8Naming
@overload
def Client(
        bitrix_token: BitrixTokenFullProtocol,
        *,
        prefer_version: Literal[1],
        timeout: Timeout = None,
        max_retries: Optional[int] = None,
        initial_retry_delay: Optional[float] = None,
        retry_delay_increment: Optional[float] = None,
        **kwargs,
) -> ClientV1: ...


# noinspection PyPep8Naming
@overload
def Client(
        bitrix_token: BitrixTokenFullProtocol,
        *,
        prefer_version: Literal[3],
        timeout: Timeout = None,
        max_retries: Optional[int] = None,
        initial_retry_delay: Optional[float] = None,
        retry_delay_increment: Optional[float] = None,
        **kwargs,
) -> ClientV3: ...


# noinspection PyPep8Naming
def Client(  # noqa: N802
        bitrix_token: BitrixTokenFullProtocol,
        *,
        prefer_version: B24APIVersionLiteral = B24APIVersion.V2,
        timeout: Timeout = None,
        max_retries: Optional[int] = None,
        initial_retry_delay: Optional[float] = None,
        retry_delay_increment: Optional[float] = None,
        **kwargs,
) -> BaseClient:
    """Factory class to create the appropriate Client version."""

    if prefer_version == ClientV1.VERSION:
        client_class = ClientV1

    elif prefer_version == ClientV2.VERSION:
        client_class = ClientV2

    elif prefer_version == ClientV3.VERSION:
        client_class = ClientV3

    else:
        raise ValueError("Invalid prefer_version, must be 1, 2 or 3")

    return client_class(
        bitrix_token=bitrix_token,
        timeout=timeout,
        max_retries=max_retries,
        initial_retry_delay=initial_retry_delay,
        retry_delay_increment=retry_delay_increment,
        **kwargs,
    )
