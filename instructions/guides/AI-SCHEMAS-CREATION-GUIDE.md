# Bitrix24 Result Schemas Creation Guide

This guide defines how to model structured Bitrix24 REST results in `b24pysdk.schemas` and connect them to value requests. It is based on the current `BaseSchema`, `BaseSchemaDict`, `BaseFileSchema`, value-request, and scope-adapter contracts.

The purpose of a schema is to provide typed, Python-friendly structured data without remote identity or lifecycle behavior. Do not create a schema merely because an API result is a dictionary.

## 1. Establish the result-shape contract first

Before generating a type or adapter, record the exact method contract:

- REST method name and API version;
- official documentation URL;
- exact raw `result` shape;
- result observed on a test portal when the call is safe;
- empty-result shape;
- required, optional, nullable, and version-dependent keys;
- exact raw type exposed by `request.result`;
- desired adapted type exposed by `request.value` or `request.values`;
- wrapper key, if any;
- selected adapter.

Use the real response as the implementation source when documentation and runtime behavior differ, and document the mismatch. If the response cannot be tested, mark the contract as documentation-only rather than guessing.

Example working record:

```text
method: crm.example.fields
documented_result: {"fields": {"FIELD": {...}}}
observed_result: {"fields": {"FIELD": {...}}}
empty_result: {"fields": {}}
raw_type: ExampleFieldsResultData
adapted_type: ExampleFieldsDict
wrapper: fields
adapter: BitrixSchemaDictAdapter(ExampleFieldsDict, wrapper="fields")
verified: yes
```

## 2. Choose the smallest correct representation

Classify the result before writing code.

### Primitive result: no schema

Do not create a schema for values already represented clearly by standard Python types:

```python
True
123
"success"
["crm", "user"]
{"CODE": "Title"}
```

Use a precise return annotation such as `bool`, `int`, `Text`, `List[Text]`, or `Dict[Text, Text]`.

### Wrapped scalar: unwrap, no schema

Do not create a class for a one-key wrapper around a scalar:

```python
{"id": 123}
{"count": 5}
{"success": True}
```

Use `BitrixResultAdapter`:

```python
result_adapter=BitrixResultAdapter(wrapper="id")
```

When conversion is also required:

```python
result_adapter=BitrixResultAdapter(
    lambda value: int_from_bitrix(value, is_required=True),
    wrapper="id",
)
```

### Standard Python conversion: no schema

If a scalar only needs conversion to `datetime`, `date`, `time`, `ZoneInfo`, `bool`, an enum, or another standard/shared Python type, use a converter through `BitrixResultAdapter`:

```python
result_adapter=BitrixResultAdapter(
    lambda value: datetime_from_bitrix(value, is_required=True),
)
```

### Derived read-only DTO: plain frozen dataclass

Use a plain frozen dataclass when the SDK assembles a convenient public value from another raw structure and that value is not itself a standalone Bitrix24 payload. This is especially important when an identifier comes from a dynamic mapping key rather than from a real `ID` field:

```python
@dataclass(**frozen_dataclass_kwargs())
class ListFieldListItem:
    """Selectable value exposed by a Bitrix24 list field."""
    bitrix_id: int
    value: Text
```

For example, `lists.field.get` exposes choices through `DISPLAY_VALUES_FORM` as `{id: value}`. The owning object hook converts each mapping pair directly into `ListFieldListItem`. Do not invent an intermediate `{"ID": ..., "VALUE": ...}` payload, a matching `TypedDict`, or `from_bitrix()`/`to_bitrix()` methods when Bitrix24 never sends or accepts that standalone shape.

A derived read-only DTO may live in the narrowest relevant `schemas` module when it is a reusable public structured value, but it is not a `BaseSchema` and must not be wired through a schema adapter.

### Structured DTO: `BaseSchema`

Use `BaseSchema` for one logical structured value that needs one or more of:

- Bitrix24-to-Python name normalization;
- scalar conversion;
- nested schema conversion;
- a typed, discoverable public result;
- conversion back to the Bitrix24 representation.

The value must correspond to a real structured Bitrix24 payload and must not have independent remote identity or lifecycle methods. If the SDK first has to invent a different dictionary shape merely to call `from_bitrix()`, use a plain derived DTO or ordinary Python value instead.

### Mapping of schema values: `BaseSchemaDict`

Use `BaseSchemaDict` when Bitrix24 returns a dictionary whose arbitrary string keys index values of one schema type:

```python
{
    "TITLE": {"type": "string", "title": "Title"},
    "PHONE": {"type": "crm_multifield", "title": "Phone"},
}
```

The result remains dictionary-like, but each value is converted to a schema.

### File value: `BaseFileSchema`

Use `BaseFileSchema` when one public value must represent both:

- a remote Bitrix24 file that can be downloaded lazily; and
- local content prepared for a later write request.

Use the existing `URLFile` directly when Bitrix24 returns a non-empty URL string and accepts the file as `[name, Base64]` on write. Create another `BaseFileSchema` subclass only when the read representation, write representation, download URL construction, or required conversion context actually differs.

### Remote entity: object, not schema

Use the object layer when the result has stable remote identity and should participate in loading, filtering, relations, updates, deletion, refresh, or local change tracking.

The presence of `filter`, `order`, or `select` is a strong signal, not an absolute rule. Identity and lifecycle semantics decide. Refer to `AI-OBJECTS-CREATION-GUIDE.md` for object generation.

## 3. `BaseSchema` contract

`BaseSchema[BSDataT]` is an abstract frozen dataclass with two required methods:

```python
@classmethod
def from_bitrix(cls, bitrix_data: BSDataT, /) -> Self:
    ...

def to_bitrix(self) -> BSDataT:
    ...
```

It deliberately does not store the original response and must not implement lifecycle methods such as `save()`, `update()`, `delete()`, or `refresh()`.

Every concrete schema must use the compatibility helper:

```python
@dataclass(**frozen_dataclass_kwargs())
class Example(BaseSchema[ExampleData]):
    ...
```

Do not repeat `frozen=True` directly. The helper is the project-wide compatibility point for supported Python versions.

Frozen dataclasses prevent rebinding attributes, but they do not deep-freeze nested lists or dictionaries. `BaseSchema` also performs no automatic copying. Materialize or copy mutable nested values explicitly when the schema must be detached from caller-owned data.

## 4. Raw result typing

### Dictionary payloads

Define a `TypedDict` for each stable dictionary shape:

```python
class ExampleData(TypedDict):
    ID: int
    NAME: Text
    ACTIVE: bool
```

The type describes raw Bitrix24 data, not converted public attributes. Preserve raw key names and raw value types exactly, including original casing.

### Missing versus nullable keys

These contracts are different:

```python
class Data(TypedDict):
    VALUE: Optional[Text]  # key is required; value may be None
```

```python
class Data(TypedDict, total=False):
    VALUE: Text  # key may be absent
```

For a mixture of required and optional keys, use an optional base:

```python
class _ExampleOptionalData(TypedDict, total=False):
    DESCRIPTION: Text
    SETTINGS: JSONDict


class ExampleData(_ExampleOptionalData):
    ID: int
    NAME: Text
```

Use `.get()` for optional or nullable scalar conversion. Use `if "KEY" in bitrix_data` when an absent key and a present empty value must be handled differently.

### Collections and aliases

Use a singular item type and a collection alias:

```python
class ExampleItemData(TypedDict):
    ID: int
    VALUE: Text


ExampleItemsData = List[ExampleItemData]
```

Use `JSONList` only for a genuinely open-ended list of JSON objects. Prefer the precise alias when the item shape is known.

For arbitrary string-keyed maps:

```python
ExampleFieldsData = Dict[Text, ExampleFieldData]
```

Do not use `TypedDict` for dynamic keys. Do not create `TypedDict` solely to describe a primitive scalar.

### Heterogeneous responses

When one method intentionally has several documented shapes, define each shape and a union:

```python
ApplicationInfoData = Union[
    ApplicationInfoOAuthData,
    ApplicationInfoWebhookData,
]
```

The adapter must select the variant using a stable discriminator or an unambiguous required key. Never select by catching arbitrary conversion exceptions.

### Literal values

When a raw Bitrix24 field accepts a finite set of serialized values, describe that transport value in the `TypedDict` through `Annotated` and the corresponding named `Literal` alias:

```python
class SonetGroupMemberData(TypedDict):
    USER_ID: Union[int, Text]
    ROLE: Annotated[Text, GroupPermissionRoleLiteral]


class _SonetGroupUserGroupOptionalData(TypedDict, total=False):
    IS_EXTRANET: Annotated[Text, B24BoolStrictLiteral]
```

The raw type must continue to describe the serialized API representation, so use `Annotated[Text, SomeLiteral]`, not the enum class itself. The public schema may expose the corresponding enum or converted Python value:

```python
@dataclass(**frozen_dataclass_kwargs())
class SonetGroupMember(BaseSchema[SonetGroupMemberData]):
    user_id: int
    role: GroupPermissionRole

    @classmethod
    def from_bitrix(cls, bitrix_data: SonetGroupMemberData, /) -> "SonetGroupMember":
        return cls(
            user_id=int_from_bitrix(bitrix_data["USER_ID"], is_required=True),
            role=GroupPermissionRole(bitrix_data["ROLE"]),
        )

    def to_bitrix(self) -> SonetGroupMemberData:
        return {
            "USER_ID": int_to_bitrix(self.user_id, is_required=True),
            "ROLE": self.role.value,
        }
```

Use the same pattern for boolean codes such as `"Y"` / `"N"`: the raw `TypedDict` field uses the appropriate literal alias, while the public dataclass field uses `bool` and conversion is performed through `bool_from_bitrix()` and `bool_to_bitrix()`.

Reuse named literal aliases from `b24pysdk.constants` (or an established shared types module only when that alias actually lives there). New serialized value domains normally belong in the appropriate module under `b24pysdk.constants` and should be exported through that constants package. Do not repeat the allowed values through an inline `Literal[...]` when a named alias already exists. Do not widen a raw field to plain `Text` when the API documents a stable finite value set, and do not use `Union[Annotated[Text, SomeLiteral], SomeEnum]`: a schema's raw type and public converted type belong to separate layers.

Do not create duplicate literal definitions in unrelated schema modules.

## 5. Standard schema template

```python
from dataclasses import dataclass
from typing import List, Optional, Text, TypedDict

from ..utils.converters import (
    bool_from_bitrix,
    bool_to_bitrix,
    int_from_bitrix,
    int_to_bitrix,
    text_from_bitrix,
    text_to_bitrix,
)
from ..utils.dataclasses import frozen_dataclass_kwargs
from ._base_schema import BaseSchema

__all__ = [
    "Example",
    "ExampleData",
]


class _ExampleOptionalData(TypedDict, total=False):
    DESCRIPTION: Text
    TAGS: List[Text]


class ExampleData(_ExampleOptionalData):
    ID: int
    NAME: Text
    ACTIVE: bool


@dataclass(**frozen_dataclass_kwargs())
class Example(BaseSchema[ExampleData]):
    """Structured result returned by ``example.get``."""

    bitrix_id: int
    name: Text
    active: bool
    description: Optional[Text]
    tags: Optional[List[Text]]

    @classmethod
    def from_bitrix(cls, bitrix_data: ExampleData, /) -> "Example":
        """Create a schema from raw Bitrix24 example data."""
        return cls(
            bitrix_id=int_from_bitrix(bitrix_data["ID"], is_required=True),
            name=text_from_bitrix(bitrix_data["NAME"], is_required=True),
            active=bool_from_bitrix(bitrix_data["ACTIVE"], is_required=True),
            description=text_from_bitrix(bitrix_data.get("DESCRIPTION")),
            tags=(
                [
                    text_from_bitrix(tag, is_required=True)
                    for tag in bitrix_data["TAGS"]
                ]
                if "TAGS" in bitrix_data
                else None
            ),
        )

    def to_bitrix(self) -> ExampleData:
        """Convert the schema to a Bitrix24-compatible dictionary."""
        bitrix_data: ExampleData = {
            "ID": int_to_bitrix(self.bitrix_id, is_required=True),
            "NAME": text_to_bitrix(self.name, is_required=True),
            "ACTIVE": bool_to_bitrix(
                self.active,
                is_required=True,
                serialize_as=bool,
            ),
        }

        if self.description is not None:
            bitrix_data["DESCRIPTION"] = text_to_bitrix(
                self.description,
                is_required=True,
            )

        if self.tags is not None:
            bitrix_data["TAGS"] = [
                text_to_bitrix(tag, is_required=True)
                for tag in self.tags
            ]

        return bitrix_data
```

Adapt key casing and boolean output format to the concrete endpoint. `serialize_as=bool`, `int`, and the default string representation are not interchangeable.

## 6. Conversion rules

### Use converters in both directions

Use the project converters whenever one exists:

| Public value | Read from Bitrix24 | Write to Bitrix24 |
|---|---|---|
| `bool` | `bool_from_bitrix` | `bool_to_bitrix` |
| `int` | `int_from_bitrix` | `int_to_bitrix` |
| `float` | `float_from_bitrix` | `float_to_bitrix` |
| `Text` | `text_from_bitrix` | `text_to_bitrix` |
| `date` | `date_from_bitrix` | `date_to_bitrix` |
| `datetime` | `datetime_from_bitrix` | `datetime_to_bitrix` |
| `time` | `time_from_bitrix` | `time_to_bitrix` |
| `ZoneInfo` | `timezone_from_bitrix` | `timezone_to_bitrix` |
| `JSONDict` | `dict_from_bitrix` | `dict_to_bitrix` |

Never use a `*_from_bitrix` converter inside `to_bitrix()`. Read converters (`*_from_bitrix`) belong only to deserialization; write converters (`*_to_bitrix`) belong to serialization. In particular, boolean serialization must use `bool_to_bitrix()` with the representation required by that endpoint, including `serialize_as=bool` for native JSON booleans when required.

Pass `is_required=True` for required public values. This makes invalid empty data fail at the schema boundary instead of silently becoming `None`.

### Enum conversion

Expose the enum in the public dataclass and preserve its raw value in `TypedDict`:

```python
status=Status(bitrix_data["STATUS"])
```

```python
"STATUS": self.status.value
```

Let the enum constructor validate unsupported raw values.

### Nested schemas

Convert nested structures explicitly:

```python
items=[
    ExampleItem.from_bitrix(item_data)
    for item_data in bitrix_data["ITEMS"]
]
```

```python
"ITEMS": [item.to_bitrix() for item in self.items]
```

For an optional nested object:

```python
details=(
    ExampleDetails.from_bitrix(bitrix_data["DETAILS"])
    if bitrix_data.get("DETAILS")
    else None
)
```

Only use truthiness when every documented empty representation means absence. If `{}`, `[]`, `0`, or `""` has a distinct meaning, check key presence and value explicitly.

### Optional output keys

Construct required output first, then add optional keys deliberately:

```python
bitrix_data: ExampleData = {
    "ID": int_to_bitrix(self.bitrix_id, is_required=True),
}

if self.description is not None:
    bitrix_data["DESCRIPTION"] = text_to_bitrix(
        self.description,
        is_required=True,
    )

return bitrix_data
```

Do not assume every public `None` should be omitted. Some APIs require `None`, an empty string, an empty list, `D`, or another sentinel. Follow the exact method contract.

### Round-trip expectations

`to_bitrix()` should produce a valid canonical Bitrix24 value of the declared `BSDataT`. It does not have to preserve irrelevant transport quirks byte-for-byte, but it must preserve meaningful data and documented empty-value semantics.

Test both directions independently. A successful `from_bitrix()` does not prove that `to_bitrix()` uses the correct names or serialization.

## 7. `BaseSchemaDict`

`BaseSchemaDict[SchemaType, RawValueType]` is a dictionary whose string keys are preserved and whose values are converted through one schema class.

```python
from typing import Dict, Text

from ._base_schema_dict import BaseSchemaDict


ExampleFieldsData = Dict[Text, ExampleFieldData]


class ExampleFieldsDict(
        BaseSchemaDict[ExampleField, ExampleFieldData],
):
    """Example field descriptions indexed by field code."""

    _VALUE_SCHEMA = ExampleField
```

The inherited methods are sufficient:

- `ExampleFieldsDict.from_bitrix(raw_mapping)` converts every value;
- `schema_dict.to_bitrix()` converts every value back;
- keys and insertion order are preserved.

`BaseSchemaDict` has no wrapper configuration. Never add `_WRAPPER` to a schema dictionary. Wrapping belongs to `BitrixSchemaDictAdapter`:

```python
result_adapter=BitrixSchemaDictAdapter(
    ExampleFieldsDict,
    wrapper="fields",
)
```

Create a distinct dictionary subclass only when the value schema differs or a distinct public type improves the API. Different wrapper keys alone do not require another subclass.

Do not use `BaseSchemaDict` for fixed-key records; use a normal `BaseSchema` plus `TypedDict` for those.

## 8. File schemas: `URLFile` and `BaseFileSchema`

`BaseFileSchema` represents remote and local file states and already implements:

- `from_bytes()`;
- `from_base64()`;
- `from_file()`;
- `from_path()`;
- lazy cached `read()` and `download()`;
- `open()`;
- `to_base64()`;
- `save_to()`;
- `name`, `extension`, and `is_local`.

### Standard URL file

`URLFile` from `b24pysdk.schemas.file` is the standard reusable schema for the common Bitrix24 contract:

- read: a direct non-empty URL string;
- write: `[name, Base64]`;
- remote content: downloaded lazily and cached;
- local content: created through the constructors inherited from `BaseFileSchema`.

Use `URLFile` directly. Do not create an entity-specific subclass only to give the same representation another name:

```python
from ..schemas.file import URLFile

image = FileField[URLFile]("IMAGE", file_class=URLFile)
personal_photo = FileField[URLFile]("PERSONAL_PHOTO", file_class=URLFile)
```

The same `URLFile` type may be reused by unrelated entities when their read and write contracts match exactly.

### Custom file schema

Create a custom `BaseFileSchema` subclass only when `URLFile` does not match the verified API contract. A concrete custom file schema must implement:

1. `from_bitrix()` for the entity's remote representation;
2. `to_bitrix()` for the entity's write representation;
3. `download_url` for remote content.

Custom template:

```python
from dataclasses import dataclass
from typing import Any, Optional, Text

from ..utils.dataclasses import frozen_dataclass_kwargs
from ..utils.types import JSONDict
from ._base_file_schema import BaseFileSchema


@dataclass(**frozen_dataclass_kwargs())
class ExampleFile(BaseFileSchema):
    url: Optional[Text] = None

    @classmethod
    def from_bitrix(
            cls,
            bitrix_data: JSONDict,
            /,
            **_context: Any,
    ) -> "ExampleFile":
        if not isinstance(bitrix_data, dict):
            raise TypeError("Bitrix24 file value must be a dictionary.")

        url = bitrix_data.get("downloadUrl")

        if not isinstance(url, str) or not url:
            raise ValueError("Bitrix24 file downloadUrl must be a non-empty string.")

        return cls(url=url)

    def to_bitrix(self) -> JSONDict:
        if self.is_local and self.name is None:
            raise ValueError("A local file requires a file name.")

        content = self.to_base64()

        if self.name is None:
            raise ValueError("Remote file name is unavailable after download.")

        return {
            "fileData": [self.name, content],
        }

    @property
    def download_url(self) -> Text:
        if self.url is None:
            raise ValueError("Local file has no download URL.")

        return self.url
```

Important rules:

- Check `URLFile` before creating another file schema. Semantic entity naming alone is not a reason to subclass it.
- The subclass must be constructible with no required arguments because local constructors call `cls()`.
- `from_bitrix()` may accept context supplied by `FileField`, such as `domain`; validate required context explicitly.
- Local content is normalized to immutable `bytes` immediately.
- `from_file()` reads from the current position and does not close the supplied stream.
- `name` and `extension` may download a remote file when no name is already known.
- `to_bitrix()` may also download a remote file if the write format embeds content.
- The downloaded bytes cache is not part of equality or hashing.
- Never assume all entities use a direct URL and `[name, Base64]`; use `URLFile` only when both sides match and otherwise implement the documented shapes.

Use the resulting class with a parameterized `FileField` so IDEs preserve the public value type:

```python
attachment = FileField[ExampleFile](
    "ATTACHMENT",
    file_class=ExampleFile,
)
```

## 9. Adapter selection

Adapters validate and normalize the outer response shape. Wrapper handling belongs to adapters, not schema classes.

### Single dictionary schema

```python
def get(...) -> BitrixAPIValueRequest[ExampleData, Example]:
    return self._make_bitrix_api_request(
        api_wrapper=self.get,
        params=params,
        timeout=timeout,
        bitrix_api_request_type=BitrixAPIValueRequest,
        result_adapter=BitrixSchemaAdapter(Example),
    )
```

Wrapped form:

```python
result_adapter=BitrixSchemaAdapter(
    Example,
    wrapper="item",
)
```

`BitrixSchemaAdapter` expects the adapted value to be a dictionary. For a scalar-backed schema such as an address or money value, use `BitrixResultAdapter(ScalarSchema.from_bitrix)` instead.

### List or generator of schemas

```python
def list(...) -> BitrixAPIValuesRequest[ExampleItemsData, ExampleItem]:
    return self._make_bitrix_api_request(
        api_wrapper=self.list,
        params=params,
        timeout=timeout,
        bitrix_api_request_type=BitrixAPIValuesRequest,
        result_adapter=BitrixSchemasAdapter(ExampleItem),
    )
```

For `{"items": [...]}`:

```python
result_adapter=BitrixSchemasAdapter(
    ExampleItem,
    wrapper="items",
)
```

`BitrixSchemasAdapter` returns:

- `[]` for raw `None`;
- a new list for a raw list;
- a generator for a raw generator;
- a list unwrapped from a configured dictionary wrapper.

It calls `Schema.from_bitrix()` for each item. There is no `BaseListableSchema` and no `Schema.from_bitrix_result()` convention.

The same adapter is preserved when a `BitrixAPIValuesRequest` is converted with `.as_list()` or `.as_list_fast()`.

### Dictionary of schemas

```python
def fields(
        ...,
) -> BitrixAPIValueRequest[ExampleFieldsData, ExampleFieldsDict]:
    return self._make_bitrix_api_request(
        api_wrapper=self.fields,
        params=params,
        timeout=timeout,
        bitrix_api_request_type=BitrixAPIValueRequest,
        result_adapter=BitrixSchemaDictAdapter(ExampleFieldsDict),
    )
```

Wrapped form:

```python
result_adapter=BitrixSchemaDictAdapter(
    ExampleFieldsDict,
    wrapper="fields",
)
```

### Scalar conversion or unwrapping

Use `BitrixResultAdapter` when the outer value is not a dictionary schema:

```python
result_adapter=BitrixResultAdapter(wrapper="count")
```

```python
result_adapter=BitrixResultAdapter(
    lambda result: Status(result),
)
```

Avoid bare lambdas when a named adapter expresses wrapper validation more clearly.

## 10. Request type contract

The two generic arguments describe different views:

```python
BitrixAPIValueRequest[RawResultType, AdaptedValueType]
BitrixAPIValuesRequest[RawCollectionType, AdaptedItemType]
```

`request.result` remains raw Bitrix24 data. `request.value` or `request.values` exposes adapted data.

Examples:

```python
BitrixAPIValueRequest[ProfileData, Profile]
BitrixAPIValuesRequest[ExampleItemsData, ExampleItem]
BitrixAPIValueRequest[ExampleFieldsResultData, ExampleFieldsDict]
BitrixAPIValueRequest[IDResultData, int]
```

For wrapped mappings, the raw generic describes the full wrapper:

```python
class ExampleFieldsResultData(TypedDict):
    fields: ExampleFieldsData
```

Do not annotate only the unwrapped value when `request.result` still contains the wrapper.

Use ordinary `BitrixAPIRequest[RawType]` when there is intentionally no adapted view.

## 11. Inheritance and variants

Use a private generic base schema only when variants genuinely share public fields and behavior:

```python
_InfoDataT = TypeVar("_InfoDataT", bound=InfoData)


@dataclass(**frozen_dataclass_kwargs())
class _BaseInfo(BaseSchema[_InfoDataT], ABC, Generic[_InfoDataT]):
    license: Text
```

Concrete variants must still implement correctly typed `from_bitrix()` and `to_bitrix()`.

Prefer composition for nested structures. Do not create inheritance merely to save a few repeated lines; it often weakens raw type precision.

For a result whose variants depend on authorization context or another stable shape discriminator, use one adapter callable that chooses the concrete schema explicitly:

```python
result_adapter=BitrixResultAdapter(
    lambda result: (
        ApplicationInfo.from_bitrix(result)
        if "ID" in result
        else WebhookInfo.from_bitrix(result)
    ),
)
```

## 12. Naming, placement, and exports

- Schema classes use singular `PascalCase`: `CRMField`, `Profile`, `URLFile`.
- Plain derived DTOs also use singular `PascalCase`, but do not use the `Data` suffix and do not pretend to implement the `BaseSchema` conversion contract.
- Raw types use `<SchemaName>Data`: `CRMFieldData`.
- Collection aliases use plural names: `CRMFieldsData`, `ExampleItemsData`.
- Dictionary schemas end in `Dict`: `CRMFieldsDict`.
- Private optional raw bases start with `_` and end in `OptionalData`.
- Use a domain prefix such as `CRM` for shared concepts where it prevents ambiguity.
- Put schemas in the narrowest stable domain module under `schemas/`.
- Put genuinely reusable constants and literals in the existing constants/types modules rather than duplicating them.
- Add all intended public schema and raw-data types to the module's `__all__`.
- Follow the package's existing export policy; do not create import cycles merely to re-export every nested schema from `schemas/__init__.py`.

Do not name a lifecycle DTO as though it were the future domain object when that would block or confuse object-layer naming. If the data is only metadata or configuration, make that role explicit in the name.

## 13. Documentation requirements

Every public schema should document:

- which REST method or response fragment it represents;
- whether it is one result, a nested value, mapping value, or file format;
- any authorization/API-version-dependent shape;
- non-obvious empty-value behavior;
- lazy download behavior for files.

Every conversion method should say what it accepts and returns. Detailed `Args`, `Returns`, and `Raises` sections are most valuable when conversion is non-trivial. Avoid empty docstrings and avoid repeating type annotations without adding behavior.

## 14. Verification checklist

### Raw typing

- Required keys are required in `TypedDict`.
- Missing keys use `total=False`; nullable values use `Optional`.
- Raw names, casing, and raw scalar types match real responses.
- Raw fields with a stable finite value set use `Annotated` with the existing named `Literal` alias; they do not use the public enum class.
- Wrapped raw types describe the full `request.result`.
- Dynamic-key maps use `Dict[Text, ValueData]`, not `TypedDict`.
- Collection aliases describe the actual item shape.

### Conversion

- Required values use converters with `is_required=True`.
- Optional and empty values follow the endpoint contract.
- `to_bitrix()` uses `*_to_bitrix`, never `*_from_bitrix`.
- Boolean output uses the correct `serialize_as` representation.
- Enums reject unknown values and serialize through `.value`.
- Nested schemas and lists convert every element in both directions.
- Mutable nested values are copied/materialized where isolation is required.
- `to_bitrix()` returns the declared raw type.
- A derived read-only DTO is built from the real owning payload without an invented intermediate `TypedDict` or unsupported `to_bitrix()` representation.

### Adapters and requests

- Single schemas use `BitrixSchemaAdapter` when the adapted payload is a dictionary.
- Schema collections use `BitrixSchemasAdapter`.
- Dynamic schema mappings use `BitrixSchemaDictAdapter`.
- Scalars and scalar wrappers use `BitrixResultAdapter`.
- Wrapper keys are configured on adapters, not schemas.
- Request generics distinguish raw result and adapted value/item.
- `.result`, `.value`, `.values`, `.as_list()`, and `.as_list_fast()` behave as annotated where applicable.
- Raw `None`, empty list, empty mapping, and missing wrapper cases are tested.

### File schemas

- Use `URLFile` directly for the standard direct-URL / `[name, Base64]` contract.
- Confirm that a custom file schema differs from `URLFile` in representation or behavior, not only in its entity-specific name.
- A custom subclass can be constructed with no required arguments.
- `from_bitrix()` validates the remote representation for both `URLFile` and custom schemas.
- Every local constructor produces the documented write representation.
- `download_url` fails clearly for a local file.
- Remote content downloads at most once per instance.
- `name`, extension, stream opening, Base64 conversion, and saving are tested.
- Entity-specific context such as portal domain is verified.

### Quality

- Run the project formatter/linter, type checker, compilation check, and tests.
- Verify IDE inference for nested schemas and parameterized `BitrixSchemaField`/`FileField` usage.
- Confirm no schema duplicates an existing shared type or a domain object.
- Confirm no adapter depends on an undocumented response shape.

## 15. Common errors

Do not:

- create a schema for `{"id": 1}` or another wrapped scalar;
- invent a standalone raw dictionary such as `{"ID": ..., "VALUE": ...}` only to make a value extracted from a dynamic mapping fit `BaseSchema`;
- classify every dictionary as a schema;
- classify every filtered/listed value as an object without checking identity;
- invent `BaseListableSchema` or `from_bitrix_result()`; they are not current contracts;
- put `_WRAPPER` on `BaseSchemaDict`; wrappers belong to adapters;
- use `bool_from_bitrix()` or another read converter in `to_bitrix()`;
- model an absent key as merely `Optional[T]`;
- widen a documented finite raw value set to plain `Text`, duplicate it with an inline `Literal`, or annotate the raw `TypedDict` field with the public enum class;
- use broad `JSONDict`/`JSONList` when the stable shape is known;
- silently treat all falsy nested values as absence;
- expose mutable raw lists or dictionaries accidentally while claiming deep immutability;
- put save/update/delete/refresh behavior in a schema;
- create an entity-specific `URLFile` subclass without a different file contract;
- store the whole original response when only converted fields are needed;
- wire a result adapter before the outer wrapper and empty-result shapes are known.

## 16. Generation workflow

For each method or coherent scope:

1. Inventory every method result before creating types.
2. Capture documented, observed, wrapped, and empty shapes.
3. Classify the result as primitive, converted scalar, derived read-only DTO, schema, schema dictionary, file, or object.
4. Reuse an existing converter, enum, schema, dictionary schema, or file schema when the contract matches exactly.
5. Define precise raw aliases and `TypedDict` structures.
6. Implement a plain frozen dataclass for a derived read-only DTO, a frozen `BaseSchema` with symmetric conversion, a minimal `BaseSchemaDict`, or a custom `BaseFileSchema` only when the existing `URLFile` contract does not match.
7. Select the adapter that matches the outer result shape.
8. Annotate both raw and adapted request views.
9. Add exports without introducing import cycles.
10. Test raw access, adapted access, empty values, invalid values, round trips, and pagination variants.

The implementation is complete only when the raw type, schema conversion, adapter, and request annotation all describe the same verified response shape.
