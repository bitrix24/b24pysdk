import inspect
from typing import TYPE_CHECKING, List, Mapping, Optional, Sequence, Text, Union, overload

from . import scopes
from .bitrix_api.protocols import BitrixTokenFullProtocol
from .bitrix_api.requests import BitrixAPIBatchesRequest, BitrixAPIBatchRequest
from .scopes._base_context import BaseContext  # noqa: protected-access
from .utils.types import JSONDict, Key, Timeout

if TYPE_CHECKING:
    from .bitrix_api.requests import BitrixAPIRequest

__all__ = [
    "Client",
]


class Client:
    """"""

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
        self.biconnector = scopes.Biconnector(self)
        self.bizproc = scopes.Bizproc(self)
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
        if hasattr(self._bitrix_token, "domain"):
            return f"<{self.__class__.__name__} of portal {self._bitrix_token.domain}>"
        else:
            return repr(self)

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
        """
        Execute multiple API requests in parallel batches.

        Args:
            bitrix_api_requests: Collection of BitrixAPIRequest objects to execute.
            halt: If True, stops processing on first error. Returns results up to that point.
            timeout: Timeout for the batches request in seconds.

        Returns:
            BitrixAPIBatchesRequest instance for executing parallel batches.
        """
        return BitrixAPIBatchesRequest(
            bitrix_token=self._bitrix_token,
            bitrix_api_requests=bitrix_api_requests,
            halt=halt,
            timeout=timeout,
            **self._kwargs,
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

    def __collect_api_methods(self, context: Union["BaseContext", "Client"]) -> List[Text]:
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
