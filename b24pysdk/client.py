"""
Bitrix API client implementations.

This module provides the main SDK client classes used to interact with
the Bitrix REST API. It includes:

- BaseClient — common functionality shared by all client versions
- ClientV1 / ClientV2 / ClientV3 — version-specific API clients
- Client — factory function that returns the appropriate client version

Each client exposes Bitrix API scopes as attributes (e.g. ``crm``, ``user``,
``task``) which provide access to the corresponding API methods.
"""

import inspect
from abc import ABC
from functools import cached_property
from typing import TYPE_CHECKING, ClassVar, List, Literal, Mapping, Optional, Sequence, Text, Union, overload

from . import scopes
from ._constants import MISSING
from .api.requests import BitrixAPIBatchesRequest, BitrixAPIBatchRequest
from .constants.version import B24APIVersion
from .protocols import BitrixTokenFullProtocol
from .scopes._base_context import BaseContext
from .utils.types import B24APIVersionLiteral, JSONDict, Key, Number, Timeout

if TYPE_CHECKING:
    from .api.requests import BitrixAPIRequest

__all__ = [
    "BaseClient",
    "Client",
    "ClientV1",
    "ClientV2",
    "ClientV3",
]


class BaseClient(ABC):
    """
    Base class for Bitrix API clients.

    Provides common functionality shared by all API client versions:

    - lazy scope access
    - lazy batch request creation
    - API method discovery
    - forwarding request configuration to API request objects

    Concrete client implementations define the Bitrix REST API version used
    for requests.
    """

    VERSION: ClassVar[Union[B24APIVersion, B24APIVersionLiteral]] = MISSING

    _bitrix_token: BitrixTokenFullProtocol
    _kwargs: JSONDict

    def __init__(
            self,
            bitrix_token: BitrixTokenFullProtocol,
            *,
            timeout: Timeout = None,
            max_retries: Optional[int] = None,
            initial_retry_delay: Optional[Number] = None,
            retry_delay_increment: Optional[Number] = None,
            **kwargs,
    ):
        """
        Initialize the Bitrix API client.

        Args:
            bitrix_token: Authentication token used to access the Bitrix REST API.
            timeout: Default request timeout.
            max_retries: Maximum number of request attempts.
            initial_retry_delay: Delay before the first retry attempt.
            retry_delay_increment: Increment added to retry delay after each attempt.
            **kwargs: Additional options passed to API request objects.
        """

        self._bitrix_token = bitrix_token

        self._kwargs = kwargs | {"prefer_version": self.VERSION}

        if timeout is not None:
            self._kwargs["timeout"] = timeout

        if max_retries is not None:
            self._kwargs["max_retries"] = max_retries

        if initial_retry_delay is not None:
            self._kwargs["initial_retry_delay"] = initial_retry_delay

        if retry_delay_increment is not None:
            self._kwargs["retry_delay_increment"] = retry_delay_increment

    @cached_property
    def access(self) -> "scopes.Access":
        return scopes.Access(self)

    @cached_property
    def ai(self) -> "scopes.AI":
        return scopes.AI(self)

    @cached_property
    def app(self) -> "scopes.App":
        return scopes.App(self)

    @cached_property
    def booking(self) -> "scopes.Booking":
        return scopes.Booking(self)

    @cached_property
    def biconnector(self) -> "scopes.Biconnector":
        return scopes.Biconnector(self)

    @cached_property
    def bizproc(self) -> "scopes.Bizproc":
        return scopes.Bizproc(self)

    @cached_property
    def calendar(self) -> "scopes.Calendar":
        return scopes.Calendar(self)

    @cached_property
    def catalog(self) -> "scopes.Catalog":
        return scopes.Catalog(self)

    @cached_property
    def crm(self) -> "scopes.CRM":
        return scopes.CRM(self)

    @cached_property
    def department(self) -> "scopes.Department":
        return scopes.Department(self)

    @cached_property
    def disk(self) -> "scopes.Disk":
        return scopes.Disk(self)

    @cached_property
    def documentgenerator(self) -> "scopes.Documentgenerator":
        return scopes.Documentgenerator(self)

    @cached_property
    def entity(self) -> "scopes.Entity":
        return scopes.Entity(self)

    @cached_property
    def event(self) -> "scopes.Event":
        return scopes.Event(self)

    @cached_property
    def events(self) -> "scopes.Events":
        return scopes.Events(self)

    @cached_property
    def feature(self) -> "scopes.Feature":
        return scopes.Feature(self)

    @cached_property
    def im(self) -> "scopes.Im":
        return scopes.Im(self)

    @cached_property
    def imbot(self) -> "scopes.Imbot":
        return scopes.Imbot(self)

    @cached_property
    def imconnector(self) -> "scopes.Imconnector":
        return scopes.Imconnector(self)

    @cached_property
    def imopenlines(self) -> "scopes.Imopenlines":
        return scopes.Imopenlines(self)

    @cached_property
    def landing(self) -> "scopes.Landing":
        return scopes.Landing(self)

    @cached_property
    def lists(self) -> "scopes.Lists":
        return scopes.Lists(self)

    @cached_property
    def mailservice(self) -> "scopes.Mailservice":
        return scopes.Mailservice(self)

    @cached_property
    def messageservice(self) -> "scopes.Messageservice":
        return scopes.Messageservice(self)

    @cached_property
    def method(self) -> "scopes.Method":
        return scopes.Method(self)

    @cached_property
    def placement(self) -> "scopes.Placement":
        return scopes.Placement(self)

    @cached_property
    def profile(self) -> "scopes.Profile":
        return scopes.Profile(self)

    @cached_property
    def pull(self) -> "scopes.Pull":
        return scopes.Pull(self)

    @cached_property
    def rpa(self) -> "scopes.Rpa":
        return scopes.Rpa(self)

    @cached_property
    def salescenter(self) -> "scopes.Salescenter":
        return scopes.Salescenter(self)

    @cached_property
    def sale(self) -> "scopes.Sale":
        return scopes.Sale(self)

    @cached_property
    def scope(self) -> "scopes.Scope":
        return scopes.Scope(self)

    @cached_property
    def server(self) -> "scopes.Server":
        return scopes.Server(self)

    @cached_property
    def sign(self) -> "scopes.Sign":
        return scopes.Sign(self)

    @cached_property
    def socialnetwork(self) -> "scopes.Socialnetwork":
        return scopes.Socialnetwork(self)

    @cached_property
    def sonet_group(self) -> "scopes.SonetGroup":
        return scopes.SonetGroup(self)

    @cached_property
    def task(self) -> "scopes.Task":
        return scopes.Task(self)

    @cached_property
    def telephony(self) -> "scopes.Telephony":
        return scopes.Telephony(self)

    @cached_property
    def timeman(self) -> "scopes.Timeman":
        return scopes.Timeman(self)

    @cached_property
    def user(self) -> "scopes.User":
        return scopes.User(self)

    @cached_property
    def userfieldconfig(self) -> "scopes.Userfieldconfig":
        return scopes.Userfieldconfig(self)

    @cached_property
    def userfieldtype(self) -> "scopes.Userfieldtype":
        return scopes.Userfieldtype(self)

    @cached_property
    def userconsent(self) -> "scopes.Userconsent":
        return scopes.Userconsent(self)

    @cached_property
    def vote(self) -> "scopes.Vote":
        return scopes.Vote(self)

    @cached_property
    def voximplant(self) -> "scopes.Voximplant":
        return scopes.Voximplant(self)

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
            *,
            halt: bool = False,
            ignore_size_limit: bool = False,
            timeout: Timeout = None,
            **kwargs,
    ) -> BitrixAPIBatchRequest[Mapping[Key, "BitrixAPIRequest"]]: ...

    @overload
    def call_batch(
            self,
            bitrix_api_requests: Sequence["BitrixAPIRequest"],
            *,
            halt: bool = False,
            ignore_size_limit: bool = False,
            timeout: Timeout = None,
            **kwargs,
    ) -> BitrixAPIBatchRequest[Sequence["BitrixAPIRequest"]]: ...

    def call_batch(
            self,
            bitrix_api_requests: Union[Mapping[Key, "BitrixAPIRequest"], Sequence["BitrixAPIRequest"]],
            *,
            halt: bool = False,
            ignore_size_limit: bool = False,
            timeout: Timeout = None,
            **kwargs,
    ) -> BitrixAPIBatchRequest:
        """
        Create a lazy request object for executing API requests in one batch.

        The request is not sent immediately. It is executed when ``call()``,
        ``response``, ``result`` or ``time`` is accessed.

        Args:
            bitrix_api_requests: Mapping or sequence of ``BitrixAPIRequest``
                objects to execute.
            halt: Whether to stop batch execution after the first failed command.
            ignore_size_limit: When ``False``, raise ``ValueError`` if the command
                collection exceeds the SDK batch limit. When ``True``, truncate
                the collection to the allowed number of commands.
            timeout: Request timeout for the batch call.
            **kwargs: Extra options overriding client-level request options.

        Returns:
            Lazy single-batch request object.
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
            bitrix_api_requests: Mapping[Key, "BitrixAPIRequest"],
            *,
            halt: bool = False,
            timeout: Timeout = None,
            **kwargs,
    ) -> BitrixAPIBatchesRequest[Mapping[Key, "BitrixAPIRequest"]]: ...

    @overload
    def call_batches(
            self,
            bitrix_api_requests: Sequence["BitrixAPIRequest"],
            *,
            halt: bool = False,
            timeout: Timeout = None,
            **kwargs,
    ) -> BitrixAPIBatchesRequest[Sequence["BitrixAPIRequest"]]: ...

    def call_batches(
            self,
            bitrix_api_requests: Union[Mapping[Key, "BitrixAPIRequest"], Sequence["BitrixAPIRequest"]],
            *,
            halt: bool = False,
            timeout: Timeout = None,
            **kwargs,
    ) -> BitrixAPIBatchesRequest:
        """
        Create a lazy request object for executing API requests across batches.

        The request is not sent immediately. It is executed when ``call()``,
        ``response``, ``result`` or ``time`` is accessed.

        Args:
            bitrix_api_requests: Mapping or sequence of ``BitrixAPIRequest``
                objects to execute.
            halt: Whether to stop batch execution after the first failed command.
            timeout: Request timeout for batch calls.
            **kwargs: Extra options overriding client-level request options.

        Returns:
            Lazy multi-batch request object.
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

    def __get_context_by_path(self, path: Text) -> "BaseContext":
        """
        Resolve a context object by dot-separated path.

        Args:
            path: Dot-separated path to the context, for example ``crm.lead``
                or ``tasks.task``.

        Returns:
            Resolved context object.

        Raises:
            ValueError: If the path is empty or cannot be resolved.
            TypeError: If the resolved object is not a ``BaseContext`` instance.
        """

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

    def __collect_api_methods(self, context: Union["BaseContext", "BaseClient"]) -> List[Text]:
        """
        Recursively collect supported API method names from a context.

        Args:
            context: Client or context object to inspect.

        Returns:
            List of available API method names.
        """

        api_methods: List[Text] = []

        for attr_name, value in inspect.getmembers(context):
            if attr_name == "__call__":
                api_methods.append(str(context))

            elif attr_name.startswith("_"):
                continue

            elif isinstance(value, BaseContext):
                api_methods.extend(self.__collect_api_methods(value))

            elif not isinstance(context, self.__class__):
                api_methods.append(f"{context}.{BaseContext._snake_to_camel(attr_name)}")

        return api_methods

    def get_supported_api_methods(self, context: Optional[Union["BaseContext", Text]] = None) -> List[Text]:
        """
        Return supported API method names.

        Args:
            context: Optional context object or dot-separated path. If omitted,
                methods from all available scopes are returned.

        Returns:
            List of available API method names.

        Raises:
            TypeError: If ``context`` is not ``None``, ``str`` or ``BaseContext``.
            ValueError: If a string path cannot be resolved.
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

        return self.__collect_api_methods(context_object)

    def print_supported_api_methods(self, context: Optional[Union["BaseContext", Text]] = None):
        """
        Print supported API method names.

        This is a convenience wrapper around ``get_supported_api_methods`` that
        prints discovered methods to stdout in sorted order, followed by the
        total number of methods.

        Args:
            context: Optional context object or dot-separated path. If omitted,
                methods from all available scopes are printed.
        """

        supported_api_methods = self.get_supported_api_methods(context)

        print("\n".join(sorted(supported_api_methods)))
        print(f"\nTotal supported API methods: {len(supported_api_methods)}")


class ClientV1(BaseClient):
    """
    Bitrix REST API v1 client.

    Provides access to API scopes supported by Bitrix REST API v1.
    """

    VERSION = B24APIVersion.V1

    @cached_property
    def tasks(self) -> "scopes.Tasks":
        return scopes.Tasks(self)


class ClientV2(ClientV1):
    """
    Bitrix REST API v2 client.

    Extends the v1 client with API methods and behavior preferred for Bitrix
    REST API v2.
    """

    VERSION = B24APIVersion.V2


class ClientV3(BaseClient):
    """
    Bitrix REST API v3 client.

    Exposes API v3 scopes and uses v3 request resolution by default.
    """

    VERSION = B24APIVersion.V3

    @cached_property
    def documentation(self) -> "scopes.v3.Documentation":
        return scopes.v3.Documentation(self)

    @cached_property
    def humanresources(self) -> "scopes.v3.Humanresources":
        return scopes.v3.Humanresources(self)

    @cached_property
    def mail(self) -> "scopes.v3.Mail":
        return scopes.v3.Mail(self)

    @cached_property
    def main(self) -> "scopes.v3.Main":
        return scopes.v3.Main(self)

    @cached_property
    def rest(self) -> "scopes.v3.Rest":
        return scopes.v3.Rest(self)

    @cached_property
    def tasks(self) -> "scopes.v3.Tasks":
        return scopes.v3.Tasks(self)


@overload
def Client(
        bitrix_token: BitrixTokenFullProtocol,
        *,
        prefer_version: Literal[2, B24APIVersion.V2] = B24APIVersion.V2,
        timeout: Timeout = None,
        max_retries: Optional[int] = None,
        initial_retry_delay: Optional[Number] = None,
        retry_delay_increment: Optional[Number] = None,
        **kwargs,
) -> ClientV2: ...


@overload
def Client(
        bitrix_token: BitrixTokenFullProtocol,
        *,
        prefer_version: Literal[1, B24APIVersion.V1],
        timeout: Timeout = None,
        max_retries: Optional[int] = None,
        initial_retry_delay: Optional[Number] = None,
        retry_delay_increment: Optional[Number] = None,
        **kwargs,
) -> ClientV1: ...


@overload
def Client(
        bitrix_token: BitrixTokenFullProtocol,
        *,
        prefer_version: Literal[3, B24APIVersion.V3],
        timeout: Timeout = None,
        max_retries: Optional[int] = None,
        initial_retry_delay: Optional[Number] = None,
        retry_delay_increment: Optional[Number] = None,
        **kwargs,
) -> ClientV3: ...


def Client(  # noqa: N802
        bitrix_token: BitrixTokenFullProtocol,
        *,
        prefer_version: Union[B24APIVersionLiteral, B24APIVersion] = B24APIVersion.V2,
        timeout: Timeout = None,
        max_retries: Optional[int] = None,
        initial_retry_delay: Optional[Number] = None,
        retry_delay_increment: Optional[Number] = None,
        **kwargs,
) -> BaseClient:
    """
    Create a Bitrix API client for the requested API version.

    Args:
        bitrix_token: Authentication token used for API access.
        prefer_version: Preferred Bitrix REST API version.
        timeout: Default request timeout.
        max_retries: Maximum number of request attempts.
        initial_retry_delay: Delay before the first retry attempt.
        retry_delay_increment: Increment added to retry delay after each attempt.
        **kwargs: Additional options passed to API request objects.

    Returns:
        Client instance corresponding to the requested API version.

    Raises:
        ValueError: If an unsupported API version is specified.
    """

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
