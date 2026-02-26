## Wrapper Classes Creation Principles

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

Each scope resides under `b24pysdk/scopes/` and is named exactly as in the Bitrix24 REST reference (https://apidocs.bitrix24.com/). The directory layout depends on whether the scope contains nested entities:

- Case 1: The scope exposes nested entities (for example, `socialnetwork.workgroup`).
  - A directory `b24pysdk/scopes/<scope_name>/` is created with the following contents:
    `b24pysdk/scopes/<scope_name>/__init__.py` — exports the public scope class inheriting from `BaseScope`.  
    `b24pysdk/scopes/<scope_name>/<entity>.py` — one file per subordinate entity, each defining exactly one `BaseEntity` subclass.

- Case 2: The scope has no subordinate entities.
  - A single file `b24pysdk/scopes/<scope_name>.py` is sufficient and contains the lone `BaseScope` subclass together with its public API methods.
  - All wrapper logic for that scope is implemented within the single class.

**Important:**
- One module must define exactly one public class.
- The class name must be the capitalized file name (`workgroup.py` → class `Workgroup`).
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

Required Structure (Correct):

Scope: b24pysdk/scopes/bizproc/__init__.py
```python
class Bizproc(BaseScope):
@cached_property
def workflow(self) -> Workflow:
    return Workflow(self)
```
Entity: b24pysdk/scopes/bizproc/workflow.py

```python
class Workflow(BaseEntity):
@cached_property
def template(self) -> Template:
    return Template(self)
```
Sub-Entity: b24pysdk/scopes/bizproc/template.py

```python
class Template(BaseEntity):
    def add(self, ...): ...
```

**Rule for Multi-Level Nesting:**
> If a REST method contains more than two segments (e.g., `scope.entity.subentity.*`), each segment beyond the scope must map to a dedicated package level: `b24pysdk/scopes/<scope>/<entity>/<subentity>/...`. This ensures the SDK’s call hierarchy (`client.<scope>.<entity>.<subentity>.*`) mirrors the REST endpoint structure exactly.
>
> For example, for methods under `entity.item.property.*`, the structure must be:
> - `b24pysdk/scopes/entity/__init__.py` → `class Entity(BaseScope)`
> - `b24pysdk/scopes/entity/item.py` → `class Item(BaseEntity)`
> - `b24pysdk/scopes/entity/item/property.py` → `class Property(BaseEntity)` with method `add()`
>
> This guarantees consistent, predictable, and IDE-friendly navigation across all scopes, regardless of depth.

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

### 4. Example of an Object Class (inherits from BaseEntity)

```python
# b24pysdk/scopes/socialnetwork/api.py
from functools import cached_property

from .._base_entity import BaseEntity
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
# b24pysdk/scopes/socialnetwork/workgroup.py
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout, B24Bool
from .._base_entity import BaseEntity

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

- **Naming:** Method names in Python must mirror the Bitrix24 REST method names. When the remote endpoint uses camelCase, define the wrapper in snake_case; the framework will convert it back to camelCase. Leading or trailing underscores are permissible when needed to avoid keyword collisions (for example, `_fields`, `import_`).
- **Signature:** Parameters documented at the top level in Bitrix24 REST documentation must be expressed in snake_case. Always include `timeout: Timeout = None`. For parameters described as arrays, annotate them with `Iterable` (or a concrete subtype) and convert them to `list` internally if necessary. Example:

```python
    params: JSONDict = {}

    if select is not None:
        if select.__class__ is not list:
            select = list(select)

        params["select"] = select
```

- **Decorator:** Annotate every public wrapper with `@type_checker` to enforce runtime validation. When methods delegate to other wrappers, apply the decorator only at the entry point to avoid redundant validation.
- **Result Formation:**
    - Assemble the `params` dictionary using native Python primitives (`int`, `float`, `bool`, `None`), standard typing hints (`Optional`, `Text`, `Iterable`), and SDK-specific helper types from `b24pysdk/utils/types` (`Timeout`, `JSONDict`, `B24Bool`, etc.) when special formatting is required. All SDK-specific helper types described in chapter 7.
    - Invoke `self._make_bitrix_api_request(...)`, providing:
      - `api_wrapper` — the current Python method, enabling `_get_api_method` to compute the REST method name.
      - `params` — omit when the endpoint accepts no payload.
      - `timeout` — propagate the caller-supplied timeout.
    - Return the resulting `BitrixAPIRequest` instance; do not perform immediate network I/O inside the wrapper.

**Example:**
```python
# b24pysdk/scopes/socialnetwork/workgroup.py
from typing import Iterable, Optional, Text, Union

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import B24BoolStrict, JSONDict, Timeout
from .._base_entity import BaseEntity

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
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "params": params,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            *,
            filter: Optional[JSONDict] = None,
            select: Optional[Iterable[Text]] = None,
            is_admin: Optional[Union[bool, B24BoolStrict]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {}

        if filter is not None:
            params["filter"] = filter

        if select is not None:
            if select.__class__ is not list:
                select = list(select)

            params["select"] = select

        if is_admin is not None:
            params["IS_ADMIN"] = B24BoolStrict(is_admin).to_b24()

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )
```

---

### 7. SDK-Specific Helper Types

The SDK provides a set of helper types in the `b24pysdk/utils/types` module. These types should be used in parameter annotations instead of basic Python types when special data processing for Bitrix24 is required.

#### Basic Type Aliases

- **`JSONDict`** — Dictionary with string keys for representing JSON structures  
- **`JSONList`** — List of `JSONDict` items for object arrays  
- **`JSONDictGenerator`** — Generator yielding `JSONDict` items  
- **`Key`** — Dictionary key (either `int` or `str`)  
- **`Number`** — Numeric value (`float` or `int`)  
- **`Timeout`** — Optional request timeout (single number or `(connect, read)` tuple)  
- **`DefaultTimeout`** — Default timeout specification  

#### Bitrix24-Specific Types

- **`B24APIResult`** — API call result type (`JSONDict`, `JSONList`, `bool`, or `None`)  
- **`B24AppStatusLiteral`** — Literal strings for Bitrix24 application statuses: `"F"` (Free), `"D"` (Demo), `"T"` (Trial), `"P"` (Paid), `"L"` (Local), `"S"` (Subscription)  
- **`B24BatchMethodTuple`** — Tuple `(api_method, params)` for batch requests  
- **`B24BatchMethods`** — Collection of batch methods (`Mapping` or `Sequence` of tuples)  
- **`UserTypeIDLiteral`** — Literal strings for CRM user field types: `"string"`, `"integer"`, `"double"`, `"date"`, `"datetime"`, `"boolean"`, `"file"`, `"enumeration"`, `"url"`, `"address"`, `"money"`, `"iblock_section"`, `"iblock_element"`, `"employee"`, `"crm"`, `"crm_status"`  

#### Validation Wrapper Classes

###### **`B24Bool`** — Three-state Bitrix24 Boolean
Represents the ternary logic used by Bitrix24 (`"Y"`/`"N"`/`"D"`).

**Conversion mapping:**
- `True` → `"Y"` (Yes)
- `False` → `"N"` (No)  
- `None` → `"D"` (Default)

**Methods:**
- `from_b24(literal: B24BoolLiteral) -> B24Bool` — Create from Bitrix24 string
- `to_b24() -> B24BoolLiteral` — Convert to Bitrix24 API format

##### **`B24BoolStrict`** — Strict Two-state Boolean (inherits `B24Bool`)
Only allows `"Y"` or `"N"` values (excludes `"D"`). Supports mathematical operations and comparisons.

**Additional features:**
- `value` property returns native Python `bool`
- Use when `"D"` (Default) is not permitted by the API endpoint

##### **`DocumentType`** — Immutable Document Type Tuple
Represents a Bitrix24 document type as a 3-element tuple.

**Structure:** `(module: str, document: str, entity: str)`  
**Validation:** Ensures exactly 3 string elements  
**Methods:** `to_b24() -> List[str]` for API serialization  
**Typing:** For parameters that will be validated using this class, specify the type as `Sequence[Text]`

##### **`B24File`** — File Attachment Wrapper
Represents a file for upload as a 2-element tuple.

**Structure:** `(filename: str, base64_content: str)`  
**Validation:** Ensures exactly 2 string elements  
**Methods:** `to_b24() -> List[str]` for API serialization  
**Typing:** For parameters that will be validated using this class, specify the type as `Sequence[Text]`

##### When using validation classes, convert parameters to the required value using `to_b24()`. Example:

```python
document_type: Optional[Sequence[Text]] = None,

if document_type is not None:
    params["DOCUMENT_TYPE"] = DocumentType(document_type).to_b24()
```

### 8. Possible Development Nuances

- 1\. When creating new scopes, conform to the established style prevalent in existing modules:
  - List function parameters one per line.
  - Declare `__all__` explicitly with the exported class.
  - Prefer `dict()` over `{}` when initializing parameter collections to maintain stylistic consistency.
  - Limit type annotations to constructs described in Section 6.
  - Use `bitrix_id` instead of `id` in your values for params
  - Leave class and method docstrings empty.
  - Methods within a class must be ordered alphabetically

- 2\. Handle boolean parameters expected as `Y`/`N` by:
  - Annotating the parameter as `bool`.
  - Converting the value with `B24Bool(<bool_value>).to_b24()` before transmission.
  
- 3\. List all mandatory parameters before the `*` separator; place optional keyword-only parameters afterwards and retrieve them with `dict.get("<param_name>")` rather than direct indexing.
  
- 4\. After implementing a new scope, expose it via `b24pysdk/_client.py` so that consumers can access it through the fluent client interface.

- 5\. If a scope method also serves as a scope for other methods, such as crm.automation.trigger, which can also invoke crm.automation.trigger.*, the __call__ method should be defined:
```python
class Trigger(BaseCRM):
    """"""

    @type_checker
    def __call__(
            self,
            *,
            target: Text,
            code: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "target": target,
        }

        if code is not None:
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
    ) -> BitrixAPIRequest:
        """"""
        return self._add(fields, timeout=timeout)

    @type_checker
    def get(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._get(bitrix_id, timeout=timeout)

    @type_checker
    def list(
            self,
            *,
            filter: Optional[JSONDict] = None,
            order: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
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
            list: Optional[JSONList] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "id": bitrix_id,
            "fields": fields,
        }

        if list is not None:
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
    ) -> BitrixAPIRequest:
        """"""
        return self._delete(bitrix_id, timeout=timeout)
```
- 7\. For parameters that accept a predefined, finite set of known string literal values, use the typing.Annotated and typing.Literal combination:
    - Annotate the parameter as Annotated[<base_type>, Literal["value1", "value2", ...]] (e.g., Annotated[Text, Literal["ASC", "DESC"]]).
    - 
- 8\. When type annotations require classes or types that are only used for static analysis or could cause circular imports or runtime overhead if imported normally, place those imports inside an if TYPE_CHECKING: block.

- 9\. Observe recurring implementation patterns found across existing scopes:
  - Lazily instantiate nested entities with `cached_property` to avoid repeated object creation while keeping attribute access ergonomic.
  - Group shared logic inside underscore-prefixed helper modules (for example, `_base_crm.py`, `_relationships/`, `_images/`) and reuse these abstractions instead of duplicating code across entities.
  - Respect the pervasive use of `__slots__` in base classes to minimise memory overhead; avoid adding dynamic attributes outside the declared slots.
  - Map Python arguments to the exact Bitrix24 parameter names (often uppercase) within `params`, mirroring the style already used in `scopes/access.py`, `scopes/crm/*`, and other modules.
  - Ensure every module maintains a clear import structure: local imports first, followed by SDK utilities (`BitrixAPIRequest`, `type_checker`, helper types) to preserve readability.

