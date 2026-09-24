## Wrapper Classes Creation Principles

This guide covers wrapper structure, public signatures, request construction, result adapters, exports, and verification. Docstring content is maintained separately in `AI-SCOPES-DOC-CREATION-GUIDE.md`; do not duplicate its templates or parameter-description rules here.

### Definition: What Is a “Scope”?
**Scope** denotes a logically coherent family of Bitrix24 REST methods that operate on the same functional area (for example, CRM, tasks, users). Scopes introduce a navigable namespace that aligns SDK objects with the REST hierarchy described in the official documentation: https://apidocs.bitrix24.com/api-reference/scopes/permissions.html. In practice, the scope corresponds to the substring preceding the first dot in an API method name—for example, the method `crm.lead.add` belongs to the `crm` scope, whereas `user.current` belongs to the `user` scope. This strict namespacing enables predictable method resolution and simplifies programmatic discovery of available operations.

### 1. Formal Definitions and Structure of Base Abstract Classes

**1.1. BaseContext**
- Serves as the abstract anchor for every invocation context (scopes, entities, sub-entities) and mediates access to shared SDK infrastructure.
- Defines uniform navigation through the object hierarchy via `_context` chaining and `_path` computation, thus providing canonical identifiers for REST method discovery.
- Implements `_get_api_method`, which converts Pythonic snake_case identifiers to the camelCase format required by Bitrix24 REST endpoints, ensuring the method naming contract between wrappers and the remote API.

**1.2. BaseScope**
- Inherits from `BaseContext` and represents every root-level scope exported to SDK consumers.
- Accepts an instance of `Client` and stores it in a dedicated slot, guaranteeing a consistent entry point to authentication credentials and request configuration.
- Supplies accessors for root operations and subordinate entities, typically exposed as lazily evaluated `cached_property` attributes for efficient reuse.

**1.3. BaseEntity**
- Inherits from `BaseContext` and models any entity nested inside a scope or another entity.
- Receives its parent context through the constructor, enabling chained resolution of scope hierarchy and configuration inheritance.
- Provides the structural template for concrete entity wrappers, including the standardized `__repr__` for debugging and tracing.

**Inheritance Hierarchy:**
- Every public scope class inherits directly from `BaseScope` (for example, `Socialnetwork`).
- Every entity class, regardless of depth in the hierarchy, inherits from `BaseEntity`.
- Additional helper abstractions (for example, `_base_crm.py`, `_base_entity.py`) are introduced where necessary to share behaviour across related entities while preserving the base contract.

---

### 2. Code Structure and Organization

Each public root scope resides under `b24pysdk/scopes/` and must expose the same public context name as the corresponding Bitrix24 REST scope (https://apidocs.bitrix24.com/). The internal Python module or package name may differ when the repository already has a justified naming convention or collision avoidance; for example, the public `client.ai` context is implemented by `b24pysdk/scopes/ai_admin/`. The public client chain and generated REST method name are authoritative. The directory layout depends on whether the scope contains nested entities:

- Case 1: The scope exposes nested entities (for example, `socialnetwork.api.workgroup`).
  - A directory `b24pysdk/scopes/<scope_name>/` is created with the following contents:
    `b24pysdk/scopes/<scope_name>/__init__.py` — exports the public scope class inheriting from `BaseScope`.  
    `b24pysdk/scopes/<scope_name>/<entity>.py` — one file per subordinate entity, each defining exactly one `BaseEntity` subclass.

- Case 2: The scope has no subordinate entities.
  - A single file `b24pysdk/scopes/<scope_name>.py` is sufficient and contains the lone `BaseScope` subclass together with its public API methods.
  - All wrapper logic for that scope is implemented within the single class.

**Important:**
- One module must define exactly one public class.
- The class name normally follows the capitalized file name (`workgroup.py` → `Workgroup`). Preserve established acronym spelling where applicable (`api.py` → `API`).
- Private or shared infrastructure intended only for internal reuse should be placed in underscore-prefixed modules (for example, `_base_crm.py`, `_productrows.py`) within the same directory.
- Each module must declare `__all__` to make the exported symbol explicit and to keep `Client` auto-completion deterministic.

Resolution Examples

Example A: Medium Depth (3 segments)

   REST Method: crm.lead.add

   SDK Call: client.crm.lead.add()

   Structure (per Case 1):
  
  - `client.crm`: Crm(BaseScope) (from crm/__init__.py)

  - `client.crm.lead`: @cached_property lead(self) -> Lead (inside Crm class)

  - `client.crm.lead.add()`: def add(...) (method inside Lead class from crm/lead.py)

Example B: Deep Nesting (4 segments) This is the canonical example for complex scopes like bizproc or socialnetwork.

REST Method: bizproc.workflow.template.add

Correct SDK Call: client.bizproc.workflow.template.add()

Incorrect SDK Call: client.bizproc.workflow.template_add()

Required Structure (current SDK layout):

Scope: `b24pysdk/scopes/bizproc/__init__.py`
```python
class Bizproc(BaseScope):
    @cached_property
    def workflow(self) -> Workflow:
        return Workflow(self)
```

Entity/package: `b24pysdk/scopes/bizproc/workflow/__init__.py`

```python
class Workflow(BaseEntity):
    @cached_property
    def template(self) -> Template:
        return Template(self)
```

Sub-entity: `b24pysdk/scopes/bizproc/workflow/template.py`

```python
class Template(BaseEntity):
    def add(self, ...): ...
```

**Rule for Multi-Level Nesting:**
> Every REST path segment beyond the root scope must map to a navigable SDK context, but it does not require a directory for every segment in all scope families. Follow the existing layout of the scope being extended.
>
> In the current `bizproc` implementation, `workflow` is a package because it owns the nested `template` context: `bizproc/workflow/__init__.py` contains `Workflow` and `bizproc/workflow/template.py` contains `Template`. The required invariant is still the public chain `client.bizproc.workflow.template.add()`.
>
> Introduce or preserve a subpackage when the existing module would conflict with a required package or when several closely related internal modules justify it. Never flatten the public API into names such as `template_add()`.

---

### 3. Example of a Scope Class (inherits from BaseScope)

```python
# b24pysdk/scopes/socialnetwork/__init__.py
from functools import cached_property

from .._base_scope import BaseScope
from .api import API

__all__ = [
    "Socialnetwork",
]


class Socialnetwork(BaseScope):
    """"""

    @cached_property
    def api(self) -> API:
        """"""
        return API(self)
```

### 4. Example of an Entity Class (inherits from BaseEntity)

```python
# b24pysdk/scopes/socialnetwork/api/__init__.py
from functools import cached_property

from ..._base_entity import BaseEntity
from .workgroup import Workgroup

__all__ = [
    "API",
]


class API(BaseEntity):
    """"""

    @cached_property
    def workgroup(self) -> Workgroup:
        """"""
        return Workgroup(self)
```

```python
# b24pysdk/scopes/socialnetwork/api/workgroup.py
from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Workgroup",
]


class Workgroup(BaseEntity):
    """"""
```

---

### 5. BaseScope → BaseEntity → ... → BaseEntity (example of a complete chain)

- Sequence: `scope.entity.subentity.method`
- Hierarchical resolution (illustrated with `Workgroup` methods):
    - `client.socialnetwork.api.workgroup.list()` → resolves to the REST method `socialnetwork.api.workgroup.list`
    - `client.socialnetwork.api.workgroup.get()` → resolves to the REST method `socialnetwork.api.workgroup.get`
- The `BaseContext._path` attribute guarantees that each link in the chain contributes its lower-case name, and `_get_api_method` appends the camelCase wrapper name to produce the final REST method identifier.
- The SDK's core principle is a strict 1-to-1 mapping between the REST method's dot-separated hierarchy and the SDK's class hierarchy.
- Each segment in the REST method name must correspond to either a nested property (@cached_property returning a BaseEntity) or the final method call.
   Warning: "Flattening" the hierarchy (e.g., turning template.add into a method named template_add) is strictly forbidden.

---

### 6. How to Add Public Wrapper Methods

- **Naming:** Method names in Python must mirror the Bitrix24 REST method names. When the remote endpoint uses camelCase, define the wrapper in snake_case; the framework will convert it back to camelCase. If the REST suffix is already a single lowercase token without camelCase boundaries (for example, `findbycomm`, `getexternallink`), keep the public wrapper name exactly as in REST and do not insert synthetic underscores or private alias helpers only to reconstruct the method name. Leading or trailing underscores are permissible when needed to avoid keyword collisions (for example, `_fields`, `import_`).
- **REST-only contract:** Add wrappers only for real Bitrix24 REST methods confirmed in the current REST documentation or MCP server. Do not add browser/frontend-only helpers such as `BX24.*` methods or UI-only JavaScript actions.
- **Signature:** Express top-level Bitrix24 parameters in `snake_case` and always include keyword-only `timeout: Timeout = None`. Required values have no default. Use `MISSING` for an omittable API parameter and test it with `is not MISSING`; use `Optional[T]` only when an explicit `None` is a valid value distinct from omission. Do not annotate `T = MISSING` as `Optional[T]` merely because it has a sentinel default.
- **Iterable parameters:** Accept `Iterable[T]` when callers may pass tuples, generators, or other one-pass iterables. Materialize exactly once before putting the value into `params`, but preserve an existing list instead of copying it:

```python
    params: JSONDict = {}

    if select is not MISSING:
        if not isinstance(select, list):
            select = list(select)

        params["select"] = select
```

- **Decorator:** Annotate every public wrapper with `@type_checker` to enforce runtime validation. When methods delegate to other wrappers, apply the decorator only at the entry point to avoid redundant validation.
- **Result Formation:**
    - Assemble the `params` dictionary using native Python primitives (`int`, `float`, `bool`, `None`), standard typing hints (`Optional`, `Text`, `Iterable`), and SDK-specific helper types from `b24pysdk/utils/types` (`Timeout`, `JSONDict`, etc.) when special formatting is required. All SDK-specific helper types described in chapter 7.
    - Declare request payloads as `params: JSONDict = {...}` or `params: JSONDict = {}`. Do not use unannotated `params = {...}` in new wrappers.
    - Annotate public boolean parameters with native `bool` or `Optional[bool]` and convert outgoing values with `bool_to_bitrix` from `b24pysdk.utils.converters`. Select the representation required by the endpoint with `serialize_as`.
    - Invoke `self._make_bitrix_api_request(...)`, providing:
      - `api_wrapper` — the current Python method, enabling `_get_api_method` to compute the REST method name.
      - `params` — omit when the endpoint accepts no payload.
      - `timeout` — propagate the caller-supplied timeout.
      - `bitrix_api_request_type` and `result_adapter` — whenever the public result is adapted to one value, several values, schemas, or SDK objects.
    - Return the resulting lazy request object; do not perform immediate network I/O inside the wrapper.
    - Keep `_make_bitrix_api_request(...)` calls multi-line even when only `api_wrapper` and `timeout` are passed.
    - Parameterize return annotations with both raw and adapted types. Use `BitrixAPIRequest[RawT]` for an unadapted response, `BitrixAPIValueRequest[RawT, ValueT]` for one adapted value, and `BitrixAPIValuesRequest[RawT, ItemT]` for an adapted collection.
    - Prefer the endpoint's exact raw result type. Use the broad `B24APIResult` union only when the endpoint can genuinely return several unrelated JSON result shapes, not as a default annotation.
    - Keep `.result` as the raw Bitrix24 response shape. Adapted requests expose `.value` or `.values`; a values request also provides `.as_list()` and `.as_list_fast()` where supported by the request layer.
    - Choose the adapter by the public contract, not merely by response shape: use result/schema adapters for scalar or schema conversion and `BitrixObjectAdapter` / `BitrixObjectsAdapter` for object results. The object adapter key must exactly match the target object's `OBJECT_KEY`, and that object module must be imported during normal SDK initialization so the registry can resolve it.
    - When a method returns one value from a known enumeration, keep the raw serialized domain as the first generic parameter and expose the enum as the adapted value: `BitrixAPIValueRequest[SomeLiteral, SomeEnum]` with `BitrixResultAdapter(SomeEnum)`. Import both the named `Literal` alias and the enum class because the enum is required at runtime by the adapter. Do not annotate such a method as `BitrixAPIRequest[SomeEnum]`: the raw `.result` remains a string, while `.value` contains the enum member.

**Example:**
```python
# b24pysdk/scopes/socialnetwork/api/workgroup.py
from typing import Iterable, Text

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.converters import bool_to_bitrix
from ....utils.functional import type_checker
from ....utils.types import JSONDict, JSONList, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Workgroup",
]


class Workgroup(BaseEntity):
    """"""

    @type_checker
    def get(
            self,
            params: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONDict]:
        """"""

        _params: JSONDict = {
            "params": params,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=_params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            *,
            filter: JSONDict = MISSING,
            select: Iterable[Text] = MISSING,
            is_admin: bool = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONList]:
        """"""

        params: JSONDict = {}

        if filter is not MISSING:
            params["filter"] = filter

        if select is not MISSING:
            if not isinstance(select, list):
                select = list(select)

            params["select"] = select

        if is_admin is not MISSING:
            params["IS_ADMIN"] = bool_to_bitrix(is_admin, is_required=True)

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )
```

For a method adapted to SDK objects, declare the values request and object adapter explicitly:

```python
@type_checker
def get(
        self,
        *,
        timeout: Timeout = None,
) -> BitrixAPIValuesRequest[JSONList, PlacementObject]:
    """"""
    return self._make_bitrix_api_request(
        api_wrapper=self.get,
        timeout=timeout,
        bitrix_api_request_type=BitrixAPIValuesRequest,
        result_adapter=BitrixObjectsAdapter("placement", client=self._client),
    )
```

Here `"placement"` must equal `PlacementObject.OBJECT_KEY`. Do not replace an object result with a plain schema merely to avoid registering or importing the object class.

For one enumerated result, declare the raw literal and adapted enum separately:

```python
from .....api.requests import BitrixAPIValueRequest
from .....constants.list import ListIBlockType, ListIBlockTypeLiteral
from ...._adapters import BitrixResultAdapter


@type_checker
def id(
        self,
        *,
        iblock_id: int = MISSING,
        iblock_code: Text = MISSING,
        timeout: Timeout = None,
) -> BitrixAPIValueRequest[ListIBlockTypeLiteral, ListIBlockType]:
    """"""

    params: JSONDict = {}

    if iblock_id is MISSING and iblock_code is MISSING:
        raise ValueError("Either 'iblock_id' or 'iblock_code' must be provided.")

    if iblock_id is not MISSING:
        params["IBLOCK_ID"] = iblock_id

    if iblock_code is not MISSING:
        params["IBLOCK_CODE"] = iblock_code

    return self._make_bitrix_api_request(
        api_wrapper=self.id,
        params=params,
        timeout=timeout,
        bitrix_api_request_type=BitrixAPIValueRequest,
        result_adapter=BitrixResultAdapter(ListIBlockType),
    )
```

In this contract, `request.result` is a `ListIBlockTypeLiteral` string returned by Bitrix24, and `request.value` is the corresponding `ListIBlockType` member.

---

### 7. SDK-Specific Helper Types

The SDK provides helper types in `b24pysdk.utils.types` and domain-specific named literals/enums under `b24pysdk.constants`. Reuse the existing type from its actual module instead of redefining the same serialized domain locally.

#### Basic Type Aliases

The following aliases live in `b24pysdk.utils.types`:

- **`JSONDict`** — Dictionary with string keys for representing one JSON object.  
- **`JSONList`** — `List[JSONDict]`. Use it only when the endpoint returns or accepts a list whose items are JSON objects; use an endpoint-specific `List[T]` for scalar item lists such as `List[int]` or `List[Text]`.  
- **`JSONGenerator`** — Generator yielding `JSONDict` items.  
- **`Key`** — Dictionary key (either `int` or `str`).  
- **`Number`** — Numeric value (`float` or `int`).  
- **`Timeout`** — Optional request timeout (single number or `(connect, read)` tuple).  
- **`DefaultTimeout`** — Default timeout specification.  
- **`B24RequestTuple`** — Tuple `(api_method, params)` for one batch request.  
- **`B24Requests`** — Collection of batch requests (`Mapping` or `Sequence` of `B24RequestTuple`).  

#### Bitrix24-Specific Types and Constants

- **`B24APIResult`** — Broad union from `b24pysdk.utils.types` used by the generic response layer for supported raw Bitrix24 result shapes. Prefer an endpoint-specific result type in wrapper annotations.  
- **`B24AppStatusLiteral`** — Application-status literal from `b24pysdk.utils.types`; reuse the existing alias instead of redefining the values in a scope.  
- **`UserTypeIDLiteral`** — CRM user-field type literal from `b24pysdk.constants.userfield`, not `b24pysdk.utils.types`. Import it from the constants package/module when required.  

#### Boolean Conversion Helpers

Use helpers from `b24pysdk.utils.converters`:

- `bool_to_bitrix(value, is_required=True)` converts a required Python `bool` to Bitrix24 `"Y"` / `"N"` by default.
- `bool_to_bitrix(value, is_required=False)` accepts `None`; with the default string representation, `None` becomes `"D"`.
- `serialize_as=int` produces `1` / `0`, while an optional `None` remains `None`.
- `serialize_as=bool` preserves native `True` / `False`, while an optional `None` remains `None`; use this for API v3 methods that expect JSON booleans.
- `bool_from_bitrix(value, is_required=True|False)` converts Bitrix24 boolean literals back to Python values for schemas and response adapters.

For request parameters documented as `Y` / `N`, annotate the wrapper argument as `bool`. Use `bool = MISSING` when the parameter may be omitted; use `Optional[bool]` only if the API also accepts an explicit null-like value. Never pass `MISSING` to the converter. After checking the sentinel, convert the value before adding it to `params`, as in `crm.item`:

```python
if use_original_uf_names is not MISSING:
    params["useOriginalUfNames"] = bool_to_bitrix(use_original_uf_names, is_required=True)
```

Set `is_required=True` when the wrapper accepts only a real boolean whenever the parameter is present. Use `is_required=False` only when explicit `None` is part of the endpoint contract. Do not replace omission with `None`: an omitted parameter must remain absent from `params`.

##### **`DocumentType`** — Immutable Document Type Tuple
Represents a Bitrix24 document type as a 3-element tuple.

**Structure:** `(module: str, document: str, entity: str)`  
**Validation:** The current runtime implementation validates that the value is a `Sequence` with exactly 3 elements. The annotation is `Sequence[Text]`, but `_validate()` does not currently inspect each element's runtime type.  
**Methods:** `to_b24() -> List[str]` for API serialization  
**Typing:** For parameters that will be validated using this class, specify the type as `Sequence[Text]`

##### **`B24File`** — File Attachment Wrapper
Represents a file for upload as a 2-element tuple.

**Structure:** `(filename: str, base64_content: str)`  
**Validation:** The current runtime implementation validates that the value is a `Sequence` with exactly 2 elements. The annotation is `Sequence[Text]`, but `_validate()` does not currently inspect each element's runtime type.  
**Methods:** `to_b24() -> List[str]` for API serialization  
**Typing:** For parameters that will be validated using this class, specify the type as `Sequence[Text]`

##### When using validation classes, convert parameters to the required value using `to_b24()`. Example:

```python
document_type: Sequence[Text] = MISSING,

if document_type is not MISSING:
    params["DOCUMENT_TYPE"] = DocumentType(document_type).to_b24()
```

### 8. Possible Development Nuances

- 1\. When creating new scopes, conform to the established style prevalent in existing modules:
  - List function parameters one per line.
  - Declare `__all__` explicitly with the exported class.
  - Do not use `dict()` for parameter collections. Initialize dictionaries with `{}`.
  - During the wrapper-generation phase, keep placeholder docstrings empty when documentation is a separate task. Final docstrings must follow `AI-SCOPES-DOC-CREATION-GUIDE.md`.
  - Use precise generic request annotations and the signature rules from Section 6.
  - Use `bitrix_id` instead of shadowing the built-in `id` in public Python signatures; map it to the exact API key inside `params`.
  - Order public methods alphabetically, while keeping navigation properties and special methods in their established structural positions.

- 2\. Handle boolean parameters through `bool_to_bitrix`:
  - Annotating the parameter as `bool`.
  - Checking `MISSING` before conversion when the parameter is omittable.
  - Selecting `serialize_as=str`, `int`, or `bool` from the exact REST contract; the default is `str`.
  - Passing `is_required=True` unless explicit `None` is a valid API value.
  
- 3\. Put required positional parameters before `*` and optional keyword-only parameters after it unless compatibility with an established public signature requires otherwise. Use `MISSING` to distinguish omission from an explicit `None`. Build `params` explicitly with `is not MISSING`; do not use `dict.get()` as a substitute for modelling omission correctly.
  
- 4\. After implementing a new root scope, wire it into the SDK's lazy scope exports and client interface:
  - add the type-only import, `__all__` entry, and `_SCOPE_MODULES` entry in `b24pysdk/scopes/__init__.py`;
  - add the corresponding `@cached_property` in `b24pysdk/client.py` on the client version(s) that support the scope;
  - for an API v3 root scope, update `b24pysdk/scopes/_v3/__init__.py` and the corresponding v3 client property instead of placing it in the v1/v2 root registry.
  Preserve the existing lazy-import pattern; do not eagerly import every scope merely to expose the new context.

- 5\. If a scope method also serves as a scope for other methods, such as crm.automation.trigger, which can also invoke crm.automation.trigger.*, the __call__ method should be defined:
```python
class Trigger(BaseCRM):
    """"""

    @type_checker
    def __call__(
            self,
            *,
            target: Text,
            code: Text = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """"""

        params: JSONDict = {
            "target": target,
        }

        if code is not MISSING:
            params["code"] = code

        return self._make_bitrix_api_request(
            api_wrapper=self,
            params=params,
            timeout=timeout,
        )
```
- 6\. If different scopes have identical methods with the same parameters, these can be abstracted into a common base class from which those classes inherit. Child classes should override parent methods by calling them using super(). This is demonstrated in b24pysdk/scopes/_base_crm.py, which defines protected methods that are subsequently called in the respective methods of subclassed entities. For example:
```python
class Userfield(BaseCRM):
    """"""

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[int]:
        """"""
        return self._add(fields, timeout=timeout)

    @type_checker
    def get(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONDict]:
        """"""
        return self._get(bitrix_id, timeout=timeout)

    @type_checker
    def list(
            self,
            *,
            filter: JSONDict = MISSING,
            order: JSONDict = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONList]:
        """"""
        return self._list(
            filter=filter,
            order=order,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            bitrix_id: int,
            fields: JSONDict,
            *,
            list: JSONList = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """"""

        params: JSONDict = {
            "id": bitrix_id,
            "fields": fields,
        }

        if list is not MISSING:
            params["LIST"] = list

        return self._make_bitrix_api_request(
            api_wrapper=self._update,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """"""
        return self._delete(bitrix_id, timeout=timeout)
```
- 7\. For parameters that accept a predefined finite set, use only `Annotated` with the project's corresponding `Literal` alias, for example `Annotated[Text, EventTypeLiteral]`. Do not use `Union[Annotated[Text, SomeLiteral], SomeEnum]`: members of `StrEnum` are already strings covered by the literal value domain. Reuse an existing constant alias instead of repeating values inline. Before adding a new type, search existing constants for the same serialized value domain and reuse the shared type when the values and meaning coincide. Add genuinely new enumerations and named `Literal` aliases to the appropriate module under `b24pysdk.constants`, export them there, and import only the literal alias into a scope wrapper unless the enum class is separately required at runtime, for example by `BitrixResultAdapter`. Group-related constants shared by `sonet_group` and `socialnetwork.api.workgroup` belong in `b24pysdk.constants.group` and use the `Group` prefix. For the permission codes `A`, `E`, and `K`, annotate wrapper parameters as `Annotated[Text, GroupPermissionRoleLiteral]`; reserve `GroupPermissionRole` for enum conversion such as `EnumField` or `BitrixResultAdapter`. Do not add a separate participant-role enum until an implemented public API requires distinct role semantics.
- 8\. When type annotations require classes or types that are only used for static analysis or could cause circular imports or runtime overhead if imported normally, place those imports inside an if TYPE_CHECKING: block.

- 9\. Observe recurring implementation patterns found across existing scopes:
  - Lazily instantiate nested entities with `cached_property` to avoid repeated object creation while keeping attribute access ergonomic.
  - Group shared logic inside underscore-prefixed helper modules (for example, `_base_crm.py`, `_relationships/`, `_images/`) and reuse these abstractions instead of duplicating code across entities.
  - Respect the pervasive use of `__slots__` in base classes to minimise memory overhead; avoid adding dynamic attributes outside the declared slots.
  - Map Python arguments to the exact Bitrix24 parameter names (often uppercase) within `params`, mirroring the style already used in `scopes/access.py`, `scopes/crm/*`, and other modules.
  - Keep imports grouped in the project order: standard-library imports, parent SDK modules (`api`, `constants`, `objects`, `schemas`, `utils`), base scope/entity modules, and finally local sibling modules.

---

### 9. Required Verification

Before considering a new or changed wrapper complete:

- Verify the generated REST method name for every public method, including snake_case-to-camelCase conversion, keyword-safe names, and `__call__` contexts.
- Verify exact request parameter keys, nesting, casing, boolean conversion, and omission. Test that `MISSING` parameters are absent and that explicit `None` is transmitted only when the endpoint supports it.
- Test required parameters, each optional parameter independently, and representative combinations. For iterable inputs, test a list, tuple, generator, and empty iterable; ensure a generator is consumed once and an existing list is not copied unnecessarily.
- Verify the return annotation, request class, and adapter together. Confirm `.result` retains the raw response while `.value` or `.values` exposes the declared adapted type.
- For an enumerated scalar result, verify that the first generic parameter is the raw named `Literal`, the second is the enum class, `BitrixResultAdapter` receives that enum class, `.result` remains the serialized string, and `.value` is the corresponding enum member.
- For object adapters, verify the `OBJECT_KEY`, import-time registration, complete/partial response handling, and client propagation into created objects.
- Verify nested contexts are cached and resolve to the exact public chain without flattened helper names.
- Export a new root scope through the lazy registry in `b24pysdk/scopes/__init__.py` (or `b24pysdk/scopes/_v3/__init__.py` for v3) and add the matching `@cached_property` in `b24pysdk/client.py`; then check imports and IDE completion.
- Run the project's formatter/linter, type checker, compilation checks, and focused wrapper tests without performing network I/O during request construction.
- Handle final class and method documentation as a separate pass using `AI-SCOPES-DOC-CREATION-GUIDE.md`.
