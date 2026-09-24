# Bitrix24 Object Classes Creation Guide

This guide defines how to add a new domain object to `b24pysdk.objects`. It is based on the current object core and its actual contracts. It covers the object class, field descriptors, the field metadata manager, the object query manager, and the adapters that connect scope responses to objects.

The goal is not to mirror every REST method. The object layer should expose a consistent, typed domain API while preserving the exact behavior and limitations of the underlying Bitrix24 endpoint.

## 1. Source-of-truth order

Before writing code, inspect all of the following:

1. The current official documentation for the entity's `get`/`list`, `add`, `update`, `delete`, and `fields` methods.
2. The current scope wrapper signatures and the exact request dictionaries they build.
3. Real response examples, including empty responses, scalar IDs, wrapper keys, nullable values, and API-version differences.
4. Existing raw result types in `schemas`, especially for methods that return a wrapper dictionary around object items.
5. Existing object core contracts in `objects/_base_object.py`, `objects/_fields`, and `objects/_managers`.
6. The closest existing object implementation only as a structural reference.

Do not infer field flags or request shapes from another entity. Bitrix24 endpoints differ in key casing, nesting, pagination, sorting, `select`, boolean serialization, and add-result shape.

## 2. Decide whether the result is an object

Create a `BaseObject` subclass when the value represents an identifiable remote entity that has:

- a stable primary key;
- a dedicated way to load one entity or filter a list by its key;
- fields that users should read and possibly change;
- object identity that should be preserved across relations and batch operations.

Use a schema instead when the value is an embedded structure without independent identity or lifecycle. Use a scalar or ordinary collection when no domain behavior is needed.

An object should not be created merely because a response is a dictionary.

## 3. Required implementation pieces

A complete object integration normally contains:

- one `BaseObject[PrimaryKeyType]` subclass, or `BaseV3Object[PrimaryKeyType]` for a REST API v3 entity;
- one concrete `BaseObjectManager` subclass, or `BaseV3ObjectManager` for a REST API v3 entity;
- optionally, one concrete `BaseFieldManager` subclass when the API exposes field metadata; use `BaseV3FieldManager` for the standard REST API v3 `*.field.get` and `*.field.list` pair;
- a raw `TypedDict` in `schemas` when a returning scope method has a known compound dictionary result;
- scope result adapters for every method returning the object;
- public exports in the object's own module and a direct runtime import from
  the scope or another actual consumer that ensures the object class is registered;
- tests for conversion, query construction, CRUD, partial selection, relations, and empty results.

The object class is registered automatically when Python creates the subclass. Therefore, its module must be imported before an adapter or string-based `ObjectField` tries to resolve its `OBJECT_KEY`. For an object declared in a nested module, import that module directly from the scope adapter or another runtime consumer. Do not import or re-export nested object modules from the parent package's `__init__.py` merely to trigger registration.

## 4. Minimal object skeleton

```python
from typing import TYPE_CHECKING, Any, Callable, Generic, Iterable, Optional, Text, TypeVar

from .._constants import MISSING
from ..utils.types import JSONDict, JSONList, Self, Timeout
from ._base_object import BaseObject
from ._fields import IntField, TextField
from ._managers import BaseObjectManager

if TYPE_CHECKING:
    from ..api.requests import BitrixAPIRequest, BitrixAPIValuesRequest
    from ..client import ClientType


class Example(BaseObject[int]):
    OBJECT_KEY = "example"
    PK = int

    objects: "ExampleManager[Self]"

    bitrix_id = IntField("ID", is_pk=True)
    name = TextField("NAME", is_required=True)

    def _get_bitrix_data(self) -> JSONDict:
        result = self.client.example.list(filter={"ID": self.bitrix_pk}).result

        if not result:
            raise self.DoesNotExist(
                f"{self.__class__.__name__} with pk={self.bitrix_pk!r} does not exist.",
            )

        if len(result) > 1:
            raise self.MultipleObjectsReturned(
                f"Multiple {self.__class__.__name__} objects returned "
                f"for pk={self.bitrix_pk!r}.",
            )

        return result[0]

    def update(self, *, name: Text = MISSING, timeout: Timeout = None) -> bool:
        fields: JSONDict = {}

        if name is not MISSING:
            fields["name"] = name

        return self._update(**fields, timeout=timeout)

    def _get_update_api_wrapper(self, client: "ClientType") -> Callable[..., "BitrixAPIRequest[bool]"]:
        return client.example.update

    def save(
            self,
            update_fields: Optional[Iterable[Text]] = None,
            *,
            timeout: Timeout = None,
    ) -> bool:
        return self._save(update_fields=update_fields, timeout=timeout)

    def delete(self, *, timeout: Timeout = None) -> bool:
        return self._delete(timeout=timeout)

    def _get_delete_api_wrapper(self, client: "ClientType") -> Callable[..., "BitrixAPIRequest[bool]"]:
        return client.example.delete


_ExampleT = TypeVar("_ExampleT", bound=Example)


class ExampleManager(BaseObjectManager[_ExampleT], Generic[_ExampleT]):
    __slots__ = ()

    def _get_api_wrapper(self, client: "ClientType") -> Callable[..., "BitrixAPIValuesRequest[JSONList, _ExampleT]"]:
        return client.example.list

    def filter(self, **filters: Any) -> Self:
        return self._filter(**filters)

    def from_pks(self, bitrix_pks: Iterable[int]) -> Self:
        return self._from_pks(bitrix_pks)


Example.objects = ExampleManager()
```

Remove unsupported public methods instead of leaving methods that fail only after a request is attempted.

## 5. Object identity and metadata

### `OBJECT_KEY`

`OBJECT_KEY` is the stable registry key used by adapters and string-based relations. It must be a non-empty string and must match the value passed to `BitrixObjectAdapter` or `BitrixObjectsAdapter`.

Use a discriminator only when several object classes intentionally share one object key. The registry contract is `ObjectDiscriminator` from `b24pysdk.utils.types`:

```python
ObjectDiscriminator = Optional[
    Union[
        Hashable,
        Tuple[Hashable, ...],
    ]
]
```

A discriminator may therefore be `None`, one hashable scalar value, or a tuple whose elements are hashable. It is not restricted to `int`. Override `get_discriminator()` with that contract:

```python
@classmethod
def get_discriminator(cls) -> ObjectDiscriminator:
    return cls.ENTITY_TYPE
```

`None` is the registry's default/fallback discriminator. Do not use `MISSING` as the base discriminator: `MISSING` models an omitted request argument, while `None` models the default registry variant.

Lookup proceeds from the most specific discriminator to less specific fallbacks. For a scalar discriminator, the candidates are the exact value and then `None`. For a tuple discriminator, the exact tuple is tried first, then non-`None` components are cumulatively replaced with `None` from right to left, and finally the scalar `None` fallback is tried. For example:

```text
("lists", 123)
("lists", None)
(None, None)
None
```

This allows a class family to register both specific and progressively more general variants. An adapter or string-based `ObjectField` must receive the same discriminator that identifies the intended object class.

When every API method for such a class family also requires the same fixed parameter, expose it separately through `get_required_class_params()`:

```python
class BaseVariant(BaseObject[int]):
    OBJECT_KEY = "variant"
    ENTITY_TYPE: ClassVar[Optional[Text]] = None

    @classmethod
    def get_discriminator(cls) -> ObjectDiscriminator:
        return cls.ENTITY_TYPE

    @classmethod
    def get_required_class_params(cls) -> JSONDict:
        return {"entity_type": cls.ENTITY_TYPE}
```

Each concrete subclass normally overrides the class constant and binds its own manager instance. It may also declare discriminator-dependent `ObjectField` projections when the base class does not yet know the discriminator required to resolve the related class. `ObjectMetadata` calls `get_required_class_params()` once while the class is created, copies the result, and exposes it as the read-only `required_class_params` mapping. The base object and manager then add those parameters automatically to ordinary list/filter, add, update, and delete requests. Fixed class parameters are not object fields and are not part of `bitrix_pk`.

Direct entity-specific calls, including `_get_bitrix_data()`, are outside the generic CRUD builders and must unpack `self._meta.required_class_params` explicitly when their wrapper requires the same parameters. Override CRUD builders only for a genuinely different endpoint shape, not merely to repeat fixed class parameters.

The list family is the reference layout for this pattern. `objects/list/_base_list.py` defines `BaseList` with `IBLOCK_TYPE_ID: Optional[ListIBlockType] = None`; concrete list classes override that value and use it as a scalar discriminator. `BaseListElement`, `BaseListField`, and `BaseListSection` define both `IBLOCK_TYPE_ID = None` and `IBLOCK_ID = None`, and return `(IBLOCK_TYPE_ID, IBLOCK_ID)` as a composite discriminator. These classes are the reference examples for tuple fallback from a specific list class to a list-type-wide class and then to the global default.

### `PK` and primary-key fields

`PK` must be a hashable type. Declare every primary-key component with `is_pk=True`. This flag makes the field read-only and non-updatable, and makes it required by default.

For one key:

```python
PK = int
bitrix_id = IntField("ID", is_pk=True)
```

For a composite key, `PK` must inherit from `BasePK` (exported publicly as `BaseBitrixPK`) and be a frozen dataclass. It must implement:

- `__post_init__()` to validate and normalize values passed to the public constructor;
- `from_bitrix()` to construct the key from raw response data;
- `to_bitrix()` to return all raw Bitrix24 key codes.

Use `_set_value()` only from `__post_init__()` when a raw-compatible constructor value must be normalized. Dataclass field names must match SDK descriptor attribute names, while `to_bitrix()` keys must exactly match the registered Bitrix24 codes. The declaration order of PK descriptors defines component order used by metadata and request construction.

```python
from dataclasses import dataclass
from typing import Text

from ..utils.converters import int_from_bitrix, int_to_bitrix, text_from_bitrix, text_to_bitrix
from ..utils.dataclasses import frozen_dataclass_kwargs
from ..utils.types import JSONDict
from ._base_pk import BasePK


@dataclass(**frozen_dataclass_kwargs())
class ExamplePK(BasePK):
    code: Text
    owner_id: int

    def __post_init__(self):
        if not isinstance(self.code, str):
            self._set_value("code", text_from_bitrix(self.code, is_required=True))

        if not isinstance(self.owner_id, int) or isinstance(self.owner_id, bool):
            self._set_value("owner_id", int_from_bitrix(self.owner_id, is_required=True))

    @classmethod
    def from_bitrix(cls, bitrix_data: JSONDict, /) -> "ExamplePK":
        return cls(
            code=bitrix_data["code"],
            owner_id=bitrix_data["ownerId"],
        )

    def to_bitrix(self) -> JSONDict:
        return {
            "code": text_to_bitrix(self.code, is_required=True),
            "ownerId": int_to_bitrix(self.owner_id, is_required=True),
        }
```

A scalar API result can construct only a scalar-PK object. A composite-PK adapter result must be a dictionary containing every required PK code. Do not expect a dataclass default to repair a missing response component: metadata represents a missing optional component as `None`, so `from_bitrix()` and `__post_init__()` must explicitly normalize that value to the public default.

For a nullable or omittable component of a composite key, opt out of requiredness explicitly:

```python
user_id = IntField("userId", is_pk=True, is_required=False)
```

This exception is valid only when the endpoint really omits that PK component and the `BasePK` implementation defines an unambiguous normalized value, such as `user_id=0`. Ordinary scalar PK fields and required composite components remain required.

Never omit PK fields from the object declaration. Adapters need them to construct object identity even for partial responses.

### Registration validation

`ObjectMetadata` rejects:

- missing or invalid `OBJECT_KEY` and `PK`;
- field attribute names containing `__`;
- duplicate concrete Bitrix24 codes;
- duplicate `ObjectField` projections for one source code;
- inline relation source fields that are not separately registered on the class.

A subclass field replaces an inherited descriptor with the same attribute name. A non-field attribute with that name removes the inherited field from metadata.

Metadata collection properties preserve declaration order and return materialized tuples. In particular, `bitrix_codes` and `pk_bitrix_codes` return `Tuple[Text, ...]`. Metadata methods that return a fixed collection of codes or request items must also return `Tuple`, not a lazy `Iterable`; keep `Iterable` for input parameters that deliberately accept generators or other one-pass values.

## 6. Field declaration rules

Field descriptors store raw values by Bitrix24 code and expose converted Python values. Attribute names are the public SDK names used by manager filters, ordering, selection, updates, and `save(update_fields=...)`.

Every documented field returned as part of an object's data must be declared as a field descriptor, including read-only values and loosely typed payloads. Do not expose a raw response field through an ad hoc `@property` that reads `self.bitrix_data`. Properties are reserved for values derived from one or more registered fields and must not replace metadata-backed fields. If an endpoint uses an additional empty-value representation for an otherwise supported field type, extend the reusable descriptor's conversion contract instead of bypassing field metadata or creating an entity-specific property.

### Object page URL

Add a read-only `url` property only when the Bitrix24 object has its own browser page. Do not add it mechanically to every object: for example, `Department` has no separate object page and therefore must not expose `url`.

Build the absolute URL from `self._base_url`, the object's primary key, and any fixed class identifiers required by the route. If an identifier such as `IBLOCK_ID` or `SOCNET_GROUP_ID` is required but may remain `None`, validate it and raise a clear `ValueError` instead of producing an invalid URL. Different object families may override `url` when their Bitrix24 routes differ.

`url` is a derived property, not a field descriptor: do not register it in object metadata, read it from `bitrix_data`, or include it in API requests. The property must not perform a hidden API request to obtain missing route parameters.

```python
@property
def url(self) -> Text:
    """Return the absolute Bitrix24 object page URL."""
    if self.IBLOCK_ID is None:
        raise ValueError("IBLOCK_ID is required to build the object URL.")

    return f"{self._base_url}/company/lists/{self.IBLOCK_ID}/element/0/{self.bitrix_pk}/"
```

### Common flags

```python
SomeField(
    "BITRIX_CODE",
    is_pk=False,
    is_required=False,
    is_multiple=False,
    is_read_only=False,
    is_updatable=True,
    request_name=None,
)
```

Specify only non-default flags.

- `is_required=True`: `None` is not a valid whole-field value. It does not mean that every add endpoint requires the parameter; the manager's explicit `add()` signature defines that contract.
- `is_multiple=True`: the public value is a list, or `None` when optional. Assignment accepts a supported iterable and materializes it. Strings, byte sequences, mappings, and `None` are not treated as multiple-value iterables.
- `is_read_only=True`: the field cannot be supplied through generic add conversion and cannot be updated.
- `is_updatable=False`: the field may be supplied during creation but cannot change afterward.
- `is_pk=True`: implies read-only and non-updatable, and is required by default. A genuinely omittable component of a composite key may explicitly set `is_required=False` and must be normalized by its `BasePK` class.
- `request_name`: explicit Python wrapper parameter name when it cannot be derived from the raw Bitrix24 code. By default, the code is converted to `snake_case`; `ID` and `id` become `bitrix_id`.

`request_name` affects request shapes that use wrapper keyword names: top-level filters and add/update parameters, and the default named-PK delete request. Nested `fields`, `filter`, `order`, and `select` structures continue to use raw Bitrix24 codes where the corresponding base builder requires them. For example, a field returned as `ID` but accepted by the list wrappers as `iblock_id` must be declared as:

```python
bitrix_id = IntField("ID", is_pk=True, request_name="iblock_id")
```

Constructor signatures of specialized descriptors must preserve this default. If a descriptor forwards `is_required=False` unconditionally, `BaseField` cannot infer requiredness from `is_pk=True`. Such constructors should accept `Optional[bool] = None` and pass it through, or every PK declaration using that descriptor must set `is_required=True` explicitly.

Use `is_read_only` for server-owned fields when the object exposes a write path on which the distinction is meaningful. If the object has no `update()`/`save()` methods and its manager exposes no bulk update operation, do not mechanically add `is_read_only=True` to every non-PK field: the absence of write methods already defines the object's read-only lifecycle. Keep the flag only where it has an independent effect, for example when generic add conversion must reject a particular server-owned field. Use `is_updatable=False` for add-only fields such as immutable type or external-code parameters. Do not mark an add-only field as read-only.

Individual `None` items are invalid in every multiple field. An empty list is valid, including for a required multiple field.

### Field type matrix

| Descriptor | Public scalar value | Use for | Important behavior |
|---|---|---|---|
| `IntField` | `int` | integer IDs and counts | Accepts integer-like API strings |
| `ListField` | `int` | ID of a portal-configured list item | Enables `FieldAccessor.items` and `display_value` |
| `FloatField` | `float` | decimal numeric values | Accepts API `int`, `float`, or numeric text |
| `TextField` | `str` | arbitrary text | Text-specific filter lookups are available |
| `HTMLField` | `str` | Bitrix24 HTML objects with `TYPE` and `TEXT` keys | Extracts `TEXT` on read; writes as ordinary text through `TextField` conversion |
| `URLField` | `str` | HTTP/HTTPS URLs | Validates URL format in both directions |
| `BoolField` | `bool` | Bitrix24 booleans | Reads `Y/N`, `0/1`, and native booleans |
| `DateField` | `date` | calendar dates | Serializes as ISO date text |
| `DateTimeField` | `datetime` | timestamps | Serializes as ISO text with seconds |
| `TimeField` | `time` | time-of-day values | Serializes as Bitrix24 time text |
| `TimeZoneField` | `ZoneInfo` | timezone identifiers | Converts to/from timezone text |
| `EnumField[E]` | enum `E` | closed string/integer value sets | Assignment also accepts the enum's raw `str`/`int` value |
| `DictField` | `JSONDict` | untyped JSON objects | Preserves loaded mapping identity, converts API `false` to `None`, and an empty API list to `{}` |
| `BitrixSchemaField[S]` | schema `S` | typed embedded structures | Uses `S.from_bitrix()` and `S.to_bitrix()` |
| `AddressField` | `Address` | Bitrix24 address strings | Uses the standard address schema |
| `MoneyField` | `Money` | Bitrix24 money strings | Uses the standard money schema |
| `FileField[F]` | file schema `F` | remote/uploadable files | Cached; use `URLFile` for direct URL / `[name, Base64]`, otherwise use the matching custom schema |
| `ObjectField[O]` | object `O` | relation through another field's PK | Cached; does not make a request on ordinary access |
| `RawField` | `Any` | undocumented opaque values with no stable structure | Performs no semantic conversion and supports no filter lookups; prefer a normal descriptor, object class, or schema whenever the contract is known |

Use `HTMLField` when Bitrix24 returns one field in this compound form:

```python
{
    "TYPE": "HTML",
    "TEXT": "<b>Test HTML</b>",
}
```

The public field value is only the `TEXT` string; `TYPE` and any other mapping keys are intentionally discarded. The converter also tolerates an already-unwrapped string, but that compatibility is not by itself a reason to choose `HTMLField`. Do not replace `TextField` merely because a string may contain HTML markup. When Bitrix24 returns the text and its type as separate fields, for example `DESCRIPTION` and `DESCRIPTION_TYPE`, keep separate descriptors.

### Boolean serialization

`BoolField` accepts all supported Bitrix24 boolean formats on read. Choose output format from the concrete endpoint documentation:

```python
legacy_flag = BoolField("ACTIVE")                 # "Y" / "N" / optional "D"
numeric_flag = BoolField("ACTIVE", serialize_as=int)   # 1 / 0
v3_flag = BoolField("active", serialize_as=bool)       # True / False
```

Do not choose `serialize_as` globally by API version unless the endpoint contract guarantees it.

Validate the read domain separately from the write documentation. If a list response can contain additional string states such as a filter mode code, the field is not a boolean even when an add/update page documents only `Y` and `N`. Use a dedicated enum or `TextField`, and constrain write methods separately.

### Enums, schemas, files, and IDE inference

Declare every enum and every named `Literal` type in the appropriate module under `b24pysdk.constants`. Do not define them in object, schema, or scope modules. The object module imports the finished constants it uses. Keep the enum and its literal alias together and export both from the constants module:

```python
# b24pysdk/constants/group.py
import typing

from ..utils import enum as _enum

__all__ = [
    "GroupType",
    "GroupTypeLiteral",
]


GroupTypeLiteral = typing.Literal[
    "group",
    "project",
    "scrum",
    "collab",
]


class GroupType(_enum.StrEnum):
    GROUP = "group"
    PROJECT = "project"
    SCRUM = "scrum"
    COLLAB = "collab"
```

Use the named literal alias from `b24pysdk.constants` in public method annotations instead of declaring an inline `Literal[...]` in the object module. Use the enum class from the same constants module as the explicit generic parameter and `enum_class` of `EnumField`.

Before adding an enum or named `Literal`, search the existing constants for the same serialized value domain. Reuse one shared type when several methods use the same values with the same meaning; do not create method- or object-specific duplicates merely because the API parameter names differ. In public method signatures, use only `Annotated[Text, SomeLiteral]`; do not add the corresponding `StrEnum` through `Union`, because `StrEnum` values are already strings covered by the literal value domain. Keep the enum class for `EnumField` conversion and use the named literal alias for accepted method arguments. Group-related constants shared by `sonet_group` and `socialnetwork.api.workgroup` belong in `b24pysdk.constants.group` and use the `Group` prefix. For the permission codes `A`, `E`, and `K`, use `GroupPermissionRole` for `EnumField` and `Annotated[Text, GroupPermissionRoleLiteral]` for public method parameters. Do not add a separate participant-role enum until an implemented public API requires distinct role semantics.

For descriptors whose public type is supplied to the constructor, explicitly parameterize the descriptor. Treat the generic parameter as mandatory even when the same class is passed to `enum_class`, `schema_class`, or `file_class`: constructor arguments do not reliably preserve the descriptor's value type in every IDE.

```python
personal_gender = EnumField[PersonalGender]("PERSONAL_GENDER", enum_class=PersonalGender)
personal_photo = FileField[URLFile]("PERSONAL_PHOTO", file_class=URLFile)
user_type = EnumField[UserType]("USER_TYPE", enum_class=UserType, is_required=True)
list = BitrixSchemaField[UserUserfieldListItem](
    "LIST",
    schema_class=UserUserfieldListItem,
    is_multiple=True,
)
```

Do not annotate the class attribute as the instance value, for example `photo: Optional[ExampleFile] = FileField(...)`. At class level it is a descriptor, and that annotation loses assignment semantics for multiple fields and can conflict with descriptor typing.

### User fields

If the Bitrix24 entity supports user-created fields, always set `_USERFIELD_BITRIX_CODE_PREFIX` on its base object class to the exact raw-code prefix returned by the API. Set it even when the SDK base class does not declare concrete user-field descriptors itself, because application subclasses may add them later.

```python
class BaseListElement(BaseObject[int]):
    _USERFIELD_BITRIX_CODE_PREFIX = "PROPERTY_"
```

For example, user custom fields use `UF_USR_`, while list-element properties use `PROPERTY_`. Leave the inherited `None` value only for entities that do not support user-created fields. Do not infer support from the descriptors currently declared on the SDK class.

### Relations

Declare the raw source descriptor first and register it as its own class attribute:

```python
department_ids = IntField("DEPARTMENT_IDS", is_multiple=True)
departments = ObjectField["Department"](
    department_ids,
    object_class="department",
)
```

Never write:

```python
departments = ObjectField(
    IntField("DEPARTMENT_IDS", is_multiple=True),
    object_class="department",
)
```

The inline source is absent from concrete-field metadata and registration fails. The separate source is required for raw conversion, writes, filtering, selection, and cache invalidation.

A relation may project a field that is also part of a composite primary key. Keep the PK descriptor registered separately and pass it to `ObjectField`; the projection does not add another PK component:

```python
user_id = IntField("userId", is_pk=True)
user = ObjectField["User"](user_id, object_class="user")
```

`object_class` may be the concrete `BaseObject` subclass or its registered string key. Prefer a string key for circular imports. It resolves lazily on first successful use and is then cached permanently on the descriptor. Ensure the related object's concrete module is imported directly by a runtime consumer before the relation is accessed; do not import a nested object module from its parent `__init__.py` for this purpose.

When a string object key is shared by several registered classes, pass the target discriminator explicitly:

```python
parent_section = ObjectField["ListSection"](
    BaseListSection.parent_section_id,
    object_class="list.section",
    discriminator=(ListIBlockType.LISTS, None),
)
```

`discriminator` is the actual `ObjectDiscriminator` value used by `Config.get_object_class()`. It is not a flag or callback, and `ObjectField` does not derive it from the class that owns the descriptor. The argument matters only for a string `object_class`; a concrete class needs no registry lookup.

Keep a discriminator-dependent relation out of a base class that does not yet know enough to resolve its target. Declare the raw source descriptor once on the base class, then declare the `ObjectField` projection in the lowest concrete subclass where the discriminator is known:

```python
class BaseListElement(BaseObject[int]):
    IBLOCK_TYPE_ID: ClassVar[Optional[ListIBlockType]] = None
    IBLOCK_ID: ClassVar[Optional[int]] = None

    iblock_section_id = IntField("IBLOCK_SECTION_ID")


class ProjectElement(ListElement):
    IBLOCK_TYPE_ID = ListIBlockType.LISTS
    IBLOCK_ID = 123

    iblock_section = ObjectField["ProjectSection"](
        BaseListElement.iblock_section_id,
        object_class="list.section",
        discriminator=(IBLOCK_TYPE_ID, IBLOCK_ID),
    )
```

Relations whose target class does not vary by discriminator, such as `created_by -> User`, belong on the base class and do not need this argument. If only a type-wide target is available, pass a partial tuple such as `(IBLOCK_TYPE_ID, None)` and rely on the documented registry fallback. A more specific application subclass may redeclare the projection with its complete discriminator.

Import the related class under `TYPE_CHECKING` so the IDE can resolve the quoted generic parameter. When the class name is used only in `ObjectField["User"]`, Ruff does not treat that string as an import usage, so suppress `F401` on the import itself:

```python
if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Placement(BaseObject[PlacementPK]):
    user_id = IntField("userId", is_pk=True)
    user = ObjectField["User"](user_id, object_class="user")
```

Do not add `# noqa: F401` mechanically. If the imported class is also used in an explicit type annotation, for example `uf_head: Optional["User"] = MISSING`, the import is already recognized as used and the suppression is unnecessary.

Reading an `ObjectField` converts source IDs to lightweight PK-only objects and does not load them. `select_related()` performs the bulk related load. A related object's manager must therefore expose callable `from_pks()`.

For a multiple relation, assignment accepts any supported iterable of related objects and stores a `BitrixObjectList`. Raw IDs should be assigned through the source descriptor, not through the object projection.

### Files

Use `URLFile` from `b24pysdk.schemas.file` directly when the API returns a direct non-empty URL and accepts `[name, Base64]` on write. Do not create entity-specific subclasses with the same behavior. Create another `BaseFileSchema` subclass only when the read representation, write representation, download URL construction, or required context differs from `URLFile`.

```python
from ..schemas.file import URLFile

personal_photo = FileField[URLFile]("PERSONAL_PHOTO", file_class=URLFile)
image = FileField[URLFile]("IMAGE", file_class=URLFile)
```

A `FileField` caches the converted file object and supplies the portal domain while converting remote metadata. Multiple file fields reject `None` items, omit optional empty items converted to `None`, and always expose a newly materialized list.

After a successful file update, the object removes stale raw file metadata and marks its data incomplete. The next file read reloads authoritative metadata from Bitrix24. Do not add entity code that manually preserves the upload payload as remote file metadata.

## 7. Object methods

### Loading one object

Implement `_get_bitrix_data()` with the narrowest documented lookup that uniquely identifies the entity. It must return one raw `JSONDict`, not an adapted object.

Use the generated class-specific exceptions:

- `self.DoesNotExist` for no result;
- `self.MultipleObjectsReturned` for more than one result.

Do not construct these exception classes manually; `BaseObject` registers them for every subclass.

The method must load complete object data. `refresh()` and missing-field fallback mark its result complete, so using a partial endpoint here would incorrectly turn absent optional fields into `None`.

When the single-object endpoint supports `select`, request every registered concrete field so a lazy reload really is complete:

```python
def _get_bitrix_data(self) -> JSONDict:
    return self.client.example.get({
        "id": self.bitrix_pk,
        "select": self._meta.bitrix_codes,
    }).result
```

`ObjectMetadata.bitrix_codes` is the declaration-ordered tuple of registered raw codes. Do not maintain a second manually synchronized “all fields” constant when the endpoint accepts those codes directly.

If different returning methods use different key casing or aliases for the same entity, normalize the raw mapping on the object, not in a general scope adapter. Override the protected `_normalize_bitrix_data()` hook and return data keyed by the registered Bitrix24 codes:

```python
from ..utils.case import camel_to_upper


_BITRIX_DATA_FIELD_ALIASES = {
    "privacyType": "PRIVACY_CODE",
}


@classmethod
def _normalize_bitrix_data(cls, bitrix_data: JSONDict, /) -> JSONDict:
    return {
        _BITRIX_DATA_FIELD_ALIASES.get(name, camel_to_upper(name)): value
        for name, value in bitrix_data.items()
    }
```

The base hook is an identity operation. It is called before metadata extracts the PK and whenever raw data is installed on the object, so both `id` and `ID` responses produce one canonical internal representation. Keep it protected: it is an internal subclass extension point used by `BaseObject` and `ObjectMetadata`, not public user API. Reuse the case helpers from `b24pysdk.utils.case` (`camel_to_snake`, `camel_to_upper`, `snake_to_camel`, and `upper_to_camel`) instead of duplicating regular expressions. Normalization must be idempotent and must not be moved into `BitrixObjectAdapter`, because response naming is entity-specific.

If the endpoint cannot filter by the full PK, load the complete collection once and match locally by normalized `bitrix_pk`. Return `DoesNotExist` for no match and `MultipleObjectsReturned` for more than one match. This is appropriate for small registration collections such as event or placement bindings; do not generalize it to large entities without checking cost.

### Update

Expose only documented, updatable parameters. Use `MISSING`, not `None`, to distinguish an omitted optional parameter from an explicit clear operation:

```python
def update(
        self,
        *,
        title: Optional[Text] = MISSING,
        timeout: Timeout = None,
) -> bool:
    fields: JSONDict = {}

    if title is not MISSING:
        fields["title"] = title

    return self._update(**fields, timeout=timeout)
```

Keys passed to `_update()` are SDK attribute names. The base method validates `is_updatable` and converts values through descriptors.

When an API accepts both a raw foreign key and an object relation, expose both but reject simultaneous use:

```python
if owner_id is not MISSING and owner is not MISSING:
    raise ValueError("Pass either owner_id or owner, not both.")
```

Implement `_get_update_api_wrapper()` only when object-level update is supported. Configure `_UPDATE_KEY` to match the scope wrapper:

- `_UPDATE_KEY = "fields"`: PK parameters at top level, changed Bitrix codes under `fields`;
- `_UPDATE_KEY = None` with no user-field prefix: PK and converted request-name values at top level;
- `_UPDATE_KEY = None` with `_USERFIELD_BITRIX_CODE_PREFIX`: one `fields` mapping with raw PK codes and raw changed codes.

### Save and local state

Expose `save()` when updates are supported. `_save(None)` sends local descriptor assignments only. `save(update_fields=[...])` takes SDK attribute names and sends their current raw values.

`DictField` deliberately returns the stored mapping rather than a defensive top-level copy. This permits an explicit in-place workflow:

```python
obj.settings["key"] = "value"
obj.save(update_fields=["settings"])
```

An in-place dictionary mutation does not create a descriptor assignment: `has_changes` remains false, `local_data` is unchanged, and parameterless `save()` does not send it. Require an explicit `update_fields` entry. Conversion on assignment still copies the caller-owned dictionary, so later mutation of the external input does not silently alter object state.

The inherited local-state API already provides:

- `has_changes`;
- `local_data` as a defensive copy;
- `reset_changes()`;
- `reset_field(name)`;
- `field(name).reset()`.

Do not duplicate this logic in generated objects.

### Delete

Expose `delete()` and `_get_delete_api_wrapper()` only when the REST API supports deletion. The default delete request converts every PK component to its descriptor's `request_name` and passes the resulting named arguments to the wrapper. It also appends `required_class_params`. Override `_make_delete_request()` only if the wrapper expects a genuinely different shape, such as positional arguments, omitted sentinel components, or an adapted count result.

When the endpoint returns a removal count rather than `bool`, do not call `_delete()`, because the default path reads `.result` as a boolean result. Build the custom request and convert its adapted value deliberately:

```python
def delete(self, *, timeout: Timeout = None) -> bool:
    return self._make_delete_request(timeout=timeout).value > 0
```

For a composite key, the default method maps every component through its field's `request_name`. A custom `_make_delete_request()` is still required when the REST contract omits a normalized sentinel component such as `user_id=0`. If one request may remove duplicate registrations, document that object deletion means “at least one matching registration was removed.”

### Object-specific API methods

An object class may expose additional immediate methods that call existing scope wrappers when the REST operation belongs to one concrete entity and requires its primary key. Do not require the caller to pass the same identifier again: obtain it from `self.bitrix_pk`.

For a scalar primary key, pass `self.bitrix_pk` as the wrapper's identifier argument:

```python
def feature_access(
        self,
        feature: Text,
        operation: Text,
        *,
        timeout: Timeout = None,
) -> bool:
    return self.client.example.feature.access(
        self.bitrix_pk,
        feature,
        operation,
        timeout=timeout,
    ).result
```

For a composite primary key, pass only the components required by the wrapper, using the public attributes of the `BasePK` value:

```python
def execute(self, *, timeout: Timeout = None) -> bool:
    return self.client.example.execute(
        self.bitrix_pk.code,
        self.bitrix_pk.owner_id,
        timeout=timeout,
    ).result
```

Use the scope wrapper's Python parameter names and return its adapted value (`.result` or `.value`, according to the request contract). Keep unrelated required API arguments as explicit method parameters and keep `timeout` keyword-only. If the operation changes fields already loaded on the object, synchronize them with `_apply_updated_data()` only after a successful result, as for `set_owner()`.

Place such a method on the object when it cannot be meaningfully invoked without the identity of that object. Keep collection-wide commands, operations on arbitrary identifiers, and calls unrelated to one loaded entity on the manager or scope. Do not duplicate request serialization or call the raw REST transport from the object: delegate to the existing typed scope wrapper.

### Field metadata hooks

Declare a field manager when the entity exposes ordinary field metadata as a mapping rather than as domain objects. The base object caches the manager's complete result in the current client's `bitrix_fields` cache under `(OBJECT_KEY, get_discriminator())`. Never key portal-specific metadata by the Python class: several registered classes may represent the same object key and discriminator, while discriminated variants sharing one `OBJECT_KEY` must remain isolated.

Some metadata endpoints return objects of another registered object type. Examples are `UserUserfield` objects used for user custom fields and `BaseListField` objects used for list elements. Load the complete collection once through the typed scope wrapper and consume `.values`, then build the lookup mapping by raw Bitrix24 field code. Store that mapping in `bitrix_objects`, not `bitrix_fields`, under the identity of the cached metadata objects:

```python
cache_key = "list.field", self.get_discriminator()
objects_cache = self.client.get_cache("bitrix_objects")
fields = objects_cache.get(cache_key)

if fields is None:
    field_objects = self.client.lists.field.get(**self._meta.required_class_params, timeout=timeout).values
    fields = {field.field_id: field for field in field_objects}
    objects_cache[cache_key] = fields
```

The cache key uses the cached object's `OBJECT_KEY`, not the consumer object's key. Thus list-field objects use `("list.field", discriminator)`, even though `get_fields()` is implemented on `BaseListElement`. If importing the metadata object at runtime creates a cycle, keep the import under `TYPE_CHECKING`, use a string annotation, and use its stable literal `OBJECT_KEY` in the cache key.

Do not request metadata separately for each field. A private single-field helper must index the mapping returned by a full-collection helper. Override `get_fields()` when the whole metadata source differs from the ordinary field-manager contract; override only `get_field()` when one subset, such as user custom fields, uses a different object-backed source.

Override `get_field_title()` only when the metadata shape supports a title, and return `str`. Override `get_field_items()` only for SDK `ListField` descriptors whose portal metadata provides choices. Do not add placeholder overrides that merely return arbitrary metadata.

Keep the metadata object's declared fields faithful to the real response. For example, `DISPLAY_VALUES_FORM` is a dynamic `{id: value}` mapping and remains a read-only `DictField` on `BaseListField`. Convert its entries into public `ListFieldListItem` values inside the consuming object's `get_field_items()` hook. Do not add an artificial `items` property to the metadata object or invent a standalone schema payload that Bitrix24 does not return.

`FieldAccessor.title`, `.items`, and `.display_value` delegate to these hooks. `display_value` expects each selectable item to expose `bitrix_id` and `value`.

## 8. Field manager

The field manager is immediate, not a lazy query builder. Use it for ordinary dictionary-like field metadata; object-backed metadata follows the `bitrix_objects` pattern described above. Its required method is `list()`:

```python
from typing import Dict, Generic, Text, TypeVar

from ..utils.types import Timeout
from ._managers import BaseFieldManager


_ExampleT = TypeVar("_ExampleT", bound=Example)


class ExampleFieldManager(BaseFieldManager[_ExampleT], Generic[_ExampleT]):
    __slots__ = ()

    def list(self, *, timeout: Timeout = None) -> Dict[Text, ExampleFieldMeta]:
        return self._client.example.fields(timeout=timeout).result


Example.fields = ExampleFieldManager()
```

The mapping must be keyed by raw Bitrix24 field code because `BaseObject.get_field()` indexes it that way. `BaseFieldManager.get(attr_name)` converts an SDK attribute name to its Bitrix code before indexing the result.

If the endpoint returns another shape, normalize it in `list()` or override the relevant lookup method deliberately. Keep the return annotation as narrow as the scope response permits.

Do not combine portal field metadata management with ordinary object queries in one manager.

### REST API v3 field metadata

Use the v3 base classes together for an entity implemented through REST API v3:

- inherit the object from `BaseV3Object`;
- inherit its query manager from `BaseV3ObjectManager`;
- inherit its field metadata manager from `BaseV3FieldManager` when both `*.field.get` and `*.field.list` exist;
- configure the object and both managers with a `ClientV3`, normally created by `Client(..., prefer_version=3)`.

`BaseV3Object` keeps the ordinary object behavior but narrows field metadata to the shared `V3Field` schema. `BaseV3ObjectManager` keeps the ordinary immutable query-builder behavior. Both bases validate the client version when the client is resolved; do not duplicate this check in concrete descendants.

The scope wrappers for v3 field methods must adapt raw metadata into `V3Field`: a single-field request exposes it through `.value`, and a list request exposes objects through `.values`. Therefore, the field manager must consume those adapted values directly and must not call `V3Field.from_bitrix()` again.

```python
from typing import TYPE_CHECKING, Callable, Generic, TypeVar

from ..schemas.v3 import V3Field, V3FieldData
from ..utils.types import JSONList
from ._base_v3_object import BaseV3Object
from ._managers import BaseV3FieldManager, BaseV3ObjectManager

if TYPE_CHECKING:
    from ..api.requests import BitrixAPIValueRequest, BitrixAPIValuesRequest
    from ..client import ClientV3


class ExampleV3(BaseV3Object[int]):
    ...


_ExampleV3T = TypeVar("_ExampleV3T", bound=ExampleV3)


class ExampleV3Manager(BaseV3ObjectManager[_ExampleV3T], Generic[_ExampleV3T]):
    ...


class ExampleV3FieldManager(BaseV3FieldManager[_ExampleV3T], Generic[_ExampleV3T]):
    def _get_api_wrapper(self, client: "ClientV3") -> Callable[..., "BitrixAPIValueRequest[V3FieldData, V3Field]"]:
        return client.example.field.get

    def _get_list_api_wrapper(self, client: "ClientV3") -> Callable[..., "BitrixAPIValuesRequest[JSONList, V3Field]"]:
        return client.example.field.list
```

Do not add a fixed field-metadata `select` in the concrete manager. The shared manager intentionally calls `field.get` with only `name` and `timeout`, and calls `field.list` with only `timeout`, so Bitrix24 returns the complete metadata shape supported by that entity.

The presence of `field.get` and `field.list` does not make CRUD, filtering, ordering, selection, pagination, or response envelopes identical across all v3 entities. Verify each concrete wrapper and expose only its real operations, just as for other objects. Set `_IS_COMPLETE_WITHOUT_SELECT = False` only when that entity's object endpoint actually returns a partial payload without `select`.

The shared v3 metadata contract does not expose selectable field values. Do not implement `get_field_items()` generically from `V3Field`; leave the base `NotImplementedError` behavior unless the concrete entity has a separate documented source for those items.

## 9. Object manager

The object manager is a copy-on-access descriptor and an immutable-style query builder. Every public query method must return a clone by delegating to a protected base method. Never mutate `_query_state` or attach result data to the class-level manager template.

### Required list wrapper

Implement `_get_api_wrapper()`:

```python
def _get_api_wrapper(
        self,
        client: "ClientType",
) -> Callable[..., "BitrixAPIValuesRequest[JSONList, _ExampleT]"]:
    return client.example.list
```

The scope method must return a `BitrixAPIValuesRequest` configured with `BitrixObjectsAdapter` for this object.

### Public query surface

Expose only operations supported by the concrete endpoint:

```python
def filter(self, **filters: Any) -> Self:
    return self._filter(**filters)

def from_pks(self, bitrix_pks: Iterable[int]) -> Self:
    return self._from_pks(bitrix_pks)

def order(self, *fields: Text) -> Self:
    return self._order(*fields)

def select(self, *fields: Text) -> Self:
    return self._select(*fields)

def select_all(self) -> Self:
    return self._select_all()

def start(self, start: Optional[int]) -> Self:
    return self._start(start)
```

`select_related()` is already public on the base manager. It becomes useful only when the object declares `ObjectField` relations and each related manager implements public `from_pks()`. A path may end with an ordinary field of a related object, for example `select_related("owner.name", "owner.email")`; those terminal fields are passed to the related manager as its nested selection.

Expose `select_all()` together with `select()` when the endpoint accepts a select list. `_select_all()` builds the selection from `ObjectMetadata.bitrix_codes` and preserves existing nested selections. Do not duplicate the registered codes in a manager constant.

Do not expose `select()` or `select_all()` when the endpoint has no `select` parameter. This does not prevent selecting fields of a related object through `select_related("relation.field")`: the parent keeps its default response fields, while the related manager receives the nested selection. Do not expose `start()` when the scope method does not accept it. Do not claim ordering support that the wrapper cannot express.

### Alternative load methods and endpoint-specific parameters

One object may be returned by several REST methods with different semantics. Keep the ordinary non-destructive list method in `_get_api_wrapper()`. Expose an alternative returning method as a dedicated manager query method that adds only its endpoint-specific parameters and switches the wrapper with `_with_api_wrapper()`.

A parameter that is not an object field and belongs only to one REST method must be declared on that dedicated method. Do not turn request controls such as `limit`, `clear`, `process_id`, or `error` into field descriptors, and do not make callers pass them through `filter()`.

```python
def get(
        self,
        *,
        limit: int = MISSING,
        clear: bool = MISSING,
        process_id: Text = MISSING,
        error: bool = MISSING,
) -> Self:
    """Return a query that reserves events through ``event.offline.get``."""

    params: JSONDict = {}

    if limit is not MISSING:
        params["limit"] = limit

    if clear is not MISSING:
        params["clear"] = clear

    if process_id is not MISSING:
        params["process_id"] = process_id

    if error is not MISSING:
        params["error"] = error

    manager = self if not params else self._with_params(**params)

    return manager._with_api_wrapper(
        lambda client: client.event.offline.get,
    ).all()
```

Call `.all()` after switching the wrapper when the alternative method is valid without parameters. `_with_api_wrapper()` changes only the resolver and does not by itself make an untouched manager executable. Preserve existing filters and ordering so chains such as `objects.filter(...).order(...).get(...)` keep their query state.

If a non-field request parameter is supported by more than one returning method, expose a chainable `with_*()` method backed by `_with_params()`:

```python
def with_auth_connector(self, auth_connector: Text) -> Self:
    """Return a query with the ``auth_connector`` request parameter."""
    return self._with_params(auth_connector=auth_connector)
```

When the scope method itself has a top-level parameter named `params` whose value is an arbitrary API-defined dictionary, keep that boundary intact and accept the complete dictionary from the caller:

```python
def with_params(self, params: JSONDict) -> Self:
    return self._with_params(params=params)
```

Do not unpack, reinterpret, or merge keys from that dictionary into manager fields. The outer keyword passed to `_with_params()` must match the scope method's parameter name. Do not override `_add_select_param()` merely to modify values inside this independent `params` mapping; the base implementation already owns the top-level `select` request parameter.

The scope wrapper remains responsible for its documented wire conversion. For example, a manager should keep `clear` and `error` as `bool` when the scope method already converts them to `0` or `1`.

### Immediate command methods

Methods that operate on a queue, reservation, binding, or processing package and return a success flag are immediate manager commands, not object queries or CRUD operations. Delegate to the existing scope wrapper and return its adapted `.result`:

```python
def clear(
        self,
        process_id: Text,
        *,
        bitrix_id: Iterable[int] = MISSING,
        message_id: Iterable[int] = MISSING,
        timeout: Timeout = None,
) -> bool:
    """Clear records from a reserved offline-event package."""
    return self._client.event.offline.clear(
        process_id,
        bitrix_id=bitrix_id,
        message_id=message_id,
        timeout=timeout,
    ).result
```

Use the same pattern for commands such as `event.offline.error`. Do not emulate these methods with `_delete()`, `_update()`, filters, or per-object requests. Keep iterable normalization in the scope wrapper when it already owns request serialization.

### Request-shape constants

Defaults are:

```python
_FILTER_KEY = "filter"
_ORDER_KEY = "order"
_SELECT_KEY = "select"
_ADD_KEY = "fields"
```

Set `_FILTER_KEY = None` when filter values belong at the request's top level. Set `_ORDER_KEY = None` when sorting is represented by top-level parameters rather than an `order` mapping. Set `_ADD_KEY = None` when add values belong at the top level and use wrapper request names rather than raw Bitrix codes.

Fixed parameters returned by the object class's `get_required_class_params()` are already merged into ordinary manager list and add requests and into object update and delete requests. Do not repeat them in each public manager method or CRUD override. Keep them out of field dictionaries: they identify the concrete class/API variant rather than object state. A custom single-object loader must still pass them explicitly because it calls a scope wrapper directly.

When a top-level API has a special sorting format such as separate `sort` and `order` parameters, override `_add_order_param()` and validate its restrictions before constructing the request. Preserve the fast-mode early return because fast pagination owns PK ordering.

### Filtering

Public filter keywords use SDK attribute names. Optional lookup suffixes are:

- `__ne`;
- `__gt`, `__gte`, `__lt`, `__lte` for ordered fields;
- `__in`, `__not_in`;
- `__contains`, `__like`, `__not_contains`, `__not_like` for text fields.

Each lookup must be supported by both the descriptor type and the object's `_FILTER_LOOKUPS`. Restrict `_FILTER_LOOKUPS` when the entity endpoint supports only a subset.

`bitrix_pk` is a synthetic filter name. Equality supports composite keys; lookup filters on it require a single PK field. `_from_pks()` creates one `bitrix_pk__in` filter and never performs one request per ID.

Consequently, do not expose the standard `from_pks()` implementation on a composite-PK manager. Add a custom bulk-key method only when one documented endpoint can accept complete composite keys without per-object requests. A composite-PK object also cannot be a normal `select_related()` target until its manager provides a compatible public bulk loader.

For endpoints with `_FILTER_KEY = None`, only the `in` lookup is supported among explicit lookups, and the generated key has no `@` prefix because the caller layer handles that top-level API shape.

If a public method needs raw endpoint-specific filters as well as typed filters, accept a positional mapping and delegate to `_filter(raw_filters, **typed_filters)`. Do not bypass descriptor conversion for ordinary declared fields.

### Ordering, selection, and fast mode

`order()` accepts SDK attribute names; a leading `-` means descending. Composite PK aliases expand to all PK fields.

`select()` accepts SDK attribute paths and always causes PK fields to be included in the actual request. A nested selection such as `owner.name` is stored for the related manager, not sent as a nested structure to the parent endpoint. If an explicit `select` is active, direct relation source fields required by `select_related()` are appended so the next level can be loaded.

Fast loading supports only complete PK ordering in one direction and does not support a `start` offset. Custom manager code must not silently discard incompatible order or start parameters.

`len(manager.as_fast())` raises because a length hint must not trigger an extra API request. Use `count()` explicitly or materialize with `to_list()`.

### `select_related()` contract

`select_related()` accepts both relation-only paths and paths ending with an ordinary field of a related object:

```python
SonetGroup.objects.using(client=client).select_related(
    "owner.name",
    "owner.last_name",
    "owner.email",
)
```

`select_related("owner")` loads `User` with its default field set. `select_related("owner.name")` loads the same relation but applies `NAME` as a `select` only on the `User` manager. Intermediate related objects do not receive an implicit `select` while their default responses are complete. Every non-terminal segment must be an `ObjectField`; after an ordinary field no further segment is allowed. A path containing no relation is invalid. This form is required when the parent endpoint has no `select` parameter but the related endpoint supports one.

For every related field, the manager:

1. Ensures that the relation source ID is available in the parent response. Without an explicit `select`, a complete default response is used unchanged. If an explicit `select` is already active or `_IS_COMPLETE_WITHOUT_SELECT = False`, only the direct relation codes requested by `select_related()` are appended. A required `select` on a manager without public `select()` raises `BitrixObjectError` before that entity request is sent.
2. Materializes parents if necessary.
3. Collects unique related PKs while preserving first-seen order.
4. Calls the related manager's public `from_pks()` once and enables fast loading.
5. Applies a terminal ordinary field as `select` only on the manager of the object that owns that field. Intermediate relation paths remain `select_related()` state.
6. Replaces cached placeholders with returned objects; missing remote rows remain PK-only placeholders.

Therefore every object intended as a relation target must have a list endpoint that can filter by a collection of IDs and a public `from_pks()` method. If terminal fields are requested, its manager must additionally expose public `select()`. Do not emulate this with a loop of single-object requests.

### Add

Expose required REST parameters as required keyword-only parameters. Omittable parameters use `MISSING`. Add `Optional[T]` only when the API also accepts an explicitly passed `None` as a value distinct from omission.

```python
def add(
        self,
        *,
        name: Text,
        description: Text = MISSING,
        timeout: Timeout = None,
) -> _ExampleT:
    fields: JSONDict = {"name": name}

    if description is not MISSING:
        fields["description"] = description

    return self._add(**fields, timeout=timeout)
```

Keys passed as keyword arguments to `_add()` are SDK attribute names and are converted through descriptors. `_get_add_params()` rejects read-only fields but accepts add-only fields.

When an endpoint moves a few registered values outside its usual `fields` mapping, override `_get_add_params()` narrowly: separate only those endpoint parameters and delegate the remaining registered fields to `super()`. The same override is used by `_add_many()`, so its input dictionaries must follow the exact same contract as public `add()`. If public `add()` accepts an endpoint-only option through positional `add_params` but `_get_add_params()` cannot derive it from each batch item, either teach the override that option or do not expose `add_many()` as equivalent.

Use the positional `add_params` mapping only for endpoint parameters that are not ordinary registered object fields:

```python
return self._add(
    {"SPECIAL_MODE": "Y"},
    name=name,
    timeout=timeout,
)
```

Validate cross-field requirements in the public manager method before calling `_add()`.

Implement `_get_add_api_wrapper()` only if creation is supported. Add-result handling accepts:

- a scalar `str` or `int` PK;
- object data containing every PK field;
- a one-key mapping wrapping either of the above.

If the real result has another shape, normalize it in the scope adapter or override the object-building hook explicitly; do not rely on accidental dictionary iteration.

Some REST methods create registrations but return only a success flag and do not return enough data to construct the object PK. Treat these as commands on the manager rather than ordinary object creation:

```python
def add(
        self,
        *,
        event: Text,
        handler: Optional[Text] = MISSING,
        timeout: Timeout = None,
) -> bool:
    params: JSONDict = {"event": event}

    if handler is not MISSING:
        params["handler"] = handler

    return self._client.event.bind(**params, timeout=timeout).result
```

In this case, do not use `_add()`, do not implement `_get_add_api_wrapper()` merely to satisfy the ordinary CRUD pattern, and do not expose `add_many()` unless a valid object-producing result contract exists. The created registration can be retrieved later through its list endpoint.

### Batch operations

Expose `add_many()` only when the same public field-dictionary contract is appropriate for batch creation. It accepts a sequence or mapping of SDK field dictionaries. Empty input returns an empty result without an API request.

Manager `update()` and `delete()` operate on the current query. The base manager selects only PK fields before bulk writes when public `select()` exists. Do not preload relations for a bulk write unless the caller explicitly preserved `select_related()` in the query.

Return the exact base result types:

- `BitrixObjectBatchAddResult[ObjectType]` for `_add_many()`;
- `BitrixObjectBatchWriteResult[ObjectType]` for query `_update()` and `_delete()`.

## 10. Binding managers to the object

Declare manager attributes in the object body for typing, then assign descriptor instances after all classes are defined:

```python
class Example(BaseObject[int]):
    fields: "ExampleFieldManager[Self]"
    objects: "ExampleManager[Self]"


Example.fields = ExampleFieldManager()
Example.objects = ExampleManager()
```

This avoids forward-definition problems and preserves the manager descriptor's generic binding. Do not share one manager instance between unrelated object classes.

## 11. Scope adapter integration

An object is not integrated until every returning scope method uses the correct adapter.

### One object or ID

```python
result_adapter=BitrixObjectAdapter(
    object_key="example",
    client=self._client,
)
```

Use `wrapper="item"` when the raw result is `{"item": ...}`. Supply `discriminator=` when the registry key is shared.

### A list or generator

```python
result_adapter=BitrixObjectsAdapter(
    object_key="example",
    client=self._client,
    select=effective_select,
)
```

When object items are nested inside a known result dictionary, type the complete raw result with a `TypedDict` in the narrowest appropriate `schemas` module. Do not leave the first request generic as `JSONDict` when the keys and value types are stable.

For `event.offline.get`, the raw result is:

```python
from typing import Optional, Text, TypedDict

from ..utils.types import JSONList

__all__ = [
    "EventOfflineGetData",
]


class EventOfflineGetData(TypedDict):
    """Raw result returned by ``event.offline.get``."""
    process_id: Optional[Text]
    events: JSONList
```

Import only this raw type into the existing scope wrapper and use it as the first generic parameter. The second parameter remains the adapted object item type:

```python
from ...schemas.event import EventOfflineGetData


def get(...) -> BitrixAPIValuesRequest[EventOfflineGetData, OfflineEventObject]:
    return self._make_bitrix_api_request(
        api_wrapper=self.get,
        params=params,
        timeout=timeout,
        bitrix_api_request_type=BitrixAPIValuesRequest,
        result_adapter=BitrixObjectsAdapter(
            "event.offline",
            client=self._client,
            wrapper="events",
        ),
    )
```

The first generic describes `request.result`; the second describes items exposed through `request.values`. The adapter's `wrapper` must exactly match the list key in the raw result. Adding this type must not rewrite unrelated request construction, conversions, documentation, or adapter behavior in an already correct scope method.

`select` has semantic meaning:

- `None` means no explicit select was sent; completeness is read from the object's metadata flag `is_complete_without_select`;
- a partial iterable means missing fields are unknown and must trigger a full reload when accessed;
- an iterable containing all registered concrete Bitrix codes means the data is complete, including the result of `select_all()`.

`BaseObject._IS_COMPLETE_WITHOUT_SELECT` defaults to `True`. Set it to `False` on an entity whose endpoint returns only a partial payload when `select` is omitted, such as an ID-only or reduced API v3 response. `ObjectMetadata` obtains the flag with `getattr(object_class, "_IS_COMPLETE_WITHOUT_SELECT", True)`, validates it, and exposes `is_complete_without_select` to adapters.

The adapter materializes a non-`None` `select` to `frozenset` once and calculates completeness once for a list result. The scope must pass the actual explicit select iterable sent to Bitrix24. Do not synthesize a default ID selection when the caller omitted `select`; pass `None` and let the metadata flag describe that endpoint's no-select behavior.

If a scope accepts an arbitrary iterable for `select`, materialize it once before putting it into request JSON and pass that same list to the adapter:

```python
if select is not MISSING:
    if not isinstance(select, list):
        select = list(select)

    params["select"] = select

adapter = BitrixObjectsAdapter(
    object_key="example",
    client=self._client,
    select=params.get("select"),
)
```

For a single-object method whose request parameters are nested inside a required `params: JSONDict`, no extra copy is needed merely to forward selection metadata:

```python
request_params = {
    "params": params,
}

return self._make_bitrix_api_request(
    api_wrapper=self.get,
    params=request_params,
    timeout=timeout,
    bitrix_api_request_type=BitrixAPIValueRequest,
    result_adapter=BitrixObjectAdapter(
        "example",
        client=self._client,
        select=params.get("select"),
    ),
)
```

`JSONDict` already requires request-ready values. `BitrixObjectAdapter` materializes the supplied selection internally. Copy or materialize it in the scope only when request construction itself needs normalization or the public signature accepts an arbitrary one-shot iterable outside a `JSONDict`.

Adapters transfer ownership of fresh API dictionaries into objects without another deep copy. Scope code and response containers must not mutate those dictionaries during adaptation. The deliberate public in-place behavior of a converted `DictField` is governed separately by the explicit `save(update_fields=[...])` contract described above.

## 12. Partial data and lazy loading

Object data has an explicit completeness state. This is essential because an absent optional field in a partial `select` is not equivalent to a real `None` value.

Field resolution order is:

1. PK from `bitrix_pk`, without loading data.
2. Local unsaved value.
3. Already loaded raw data.
4. One complete reload if the field is absent from partial data.
5. `None` for an absent optional field in complete data, or `BitrixObjectFieldNotLoadedError` for an absent required field.

Object generators and managers must not overwrite this state after adaptation. Correctness belongs at the adapter boundary through effective `select`.

## 13. Naming, typing, and formatting rules

- Object classes use singular `PascalCase`: `Department`, `UserUserfield`.
- Object managers use `<Object>Manager`.
- Field managers use `<Object>FieldManager`.
- SDK field attributes use `snake_case`.
- Raw Bitrix24 field codes preserve documented casing exactly.
- Use `bitrix_id` for a Bitrix code equal to `ID` or `id`; this also matches the generated request name.
- Use `Text` consistently with the current module style.
- Use `Self` for object-bound or manager-chain return types where appropriate.
- Use a bounded private manager type variable, such as `_ExampleT`, to preserve subclass-aware results.
- Import enums and named `Literal` aliases from `b24pysdk.constants`; never declare them in an object module.
- Put imports used only in annotations under `TYPE_CHECKING` when runtime resolution is not required. Add `# noqa: F401` when an import is needed only to resolve a quoted `ObjectField` generic and is otherwise unused; omit the suppression when an explicit annotation already references the type.
- For circular relations, parameterize `ObjectField` with a quoted type and use a string registry key.
- Prefer precise public method parameter types. Use `Any` only for intentionally open field dictionaries or genuinely untyped API values.
- Never use mutable default arguments.

Format every function or method declaration according to the number of declared parameters:

- with one or two parameters, keep the complete declaration on one line;
- with three or more parameters, place the opening parenthesis after the function name, put every parameter on its own line, and put the closing parenthesis with the return annotation on a separate line.

Count `self` and `cls` as parameters. Do not count the positional-only marker `/` or keyword-only marker `*` as parameters.

```python
def _get_api_wrapper(self, client: "ClientType") -> Callable[..., "BitrixAPIValuesRequest[Any, BOT]"]:
    ...


def delete(self, *, timeout: Timeout = None) -> bool:
    ...


def update(
        self,
        name: Text = MISSING,
        *,
        timeout: Timeout = None,
) -> bool:
    ...
```

Apply the same rule to function and method calls according to the number of supplied positional and keyword arguments:

- with one or two arguments, keep the complete call on one line;
- with three or more arguments, put every argument on its own line and the closing parenthesis on a separate line.

Do not count the callable itself as an argument.

```python
return self._delete(timeout=timeout)

return self._get_object(bitrix_id, timeout=timeout)

return self.client.example.update(
    self.bitrix_pk,
    fields,
    timeout=timeout,
).result
```

`MISSING` and `Optional` describe different things. `MISSING` means the caller may omit a parameter. `Optional[T]` means the caller may explicitly pass `None`. Do not add `Optional` merely because an argument has a `MISSING` default; use it only when the REST method or object field accepts an explicit null value.

For multiple public inputs, annotate `Iterable[T]` when generators and tuples are valid. The field layer materializes supported iterables. Use `List[T]` only when the public contract intentionally requires an actual mutable/materialized list.

## 14. Exports and import order

After defining the object:

1. Add object, manager, and field-manager names to that module's `__all__`. Reusable internal descriptors may be exported from `objects/_fields/__init__.py` without being added to the public `objects/__init__.py` surface.
2. Keep each package `__init__.py` limited to the classes implemented in that file. Do not import or re-export classes and managers from nested object files. For example, `objects/event/__init__.py` must not contain `from .offline import OfflineEvent, OfflineEventManager`.
3. Ensure the nested module is imported directly by its scope adapter or another real runtime consumer before adapters resolve `OBJECT_KEY` or relations resolve string keys. For example, the offline-event scope imports `OfflineEvent` from `objects.event.offline`.
4. Avoid runtime circular imports. Use `TYPE_CHECKING` imports and string relation keys when possible.

An unused type-only relation import may still be needed by static analysis, but it does not register the class at runtime. Registration must come from a direct runtime import of the concrete module by the code that consumes it, not from a convenience import in the parent `__init__.py`.

## 15. Generation workflow

Use this order for each new entity:

1. Record exact response shapes and request shapes for all relevant methods.
2. Decide whether the value is an object rather than a schema.
3. Choose `OBJECT_KEY`, `PK`, and every PK descriptor.
4. If several classes share `OBJECT_KEY`, choose a stable discriminator, define any fixed request parameters through `get_required_class_params()`, and decide the base/concrete module layout before declaring fields.
5. Build a field table with Bitrix code, SDK name, descriptor, requiredness, multiplicity, read-only status, update status, explicit `request_name` where needed, and outgoing boolean representation.
6. Add every required enum and named `Literal` alias to the appropriate `b24pysdk.constants` module and export it there.
7. Declare all concrete fields, importing enum and literal types from `b24pysdk.constants`.
8. Add relation projections only after their source descriptors exist. Put discriminator-dependent projections in the lowest subclass where the target discriminator is known and pass it explicitly to `ObjectField`.
9. Implement complete single-object loading, requesting `ObjectMetadata.bitrix_codes` when the endpoint requires an explicit select for a complete response.
10. Add object-level raw-key normalization when returning methods use different casing or aliases; keep adapters entity-agnostic.
11. Implement only supported object-level update, save, delete, entity-bound API methods, and metadata hooks.
12. Implement the field manager if a metadata endpoint exists.
13. Implement the object manager's supported public query methods and request-shape constants/overrides.
14. Implement add and bulk methods with explicit required parameters and `MISSING` optionals.
15. Bind managers after class definitions; bind a separate inherited manager class/instance for every concrete member of a discriminated family.
16. Add a raw `TypedDict` for every known compound returning result and use it as the scope request's first generic parameter.
17. Connect all returning scope methods to adapters, forwarding the matching discriminator, explicit `select`, the correct no-select completeness flag, and the exact wrapper key for nested item lists.
18. Add endpoint-specific manager query methods and immediate commands that cannot be represented by ordinary fields or CRUD helpers.
19. Add exports to the object's own module and verify registration through a direct runtime import of that module; do not add nested-module imports to a parent `__init__.py`.
20. Apply the declaration/call formatting rule: one line for up to two parameters or arguments, and one item per line for three or more.
21. Test runtime behavior, typing, and request count.

## 16. Required verification

### Object and fields

- Construct from PK without an API request.
- Construct from complete data and from partial selected data.
- Verify every scalar conversion in both directions.
- Verify optional, required, multiple, empty-list, and invalid `None`-item behavior.
- Verify `is_read_only` and add-only `is_updatable=False` behavior.
- Verify that every `EnumField`, `FileField`, `ObjectField`, and `BitrixSchemaField` has an explicit generic parameter, then check its IDE result and assignment types.
- For an `ObjectField` projected from a PK descriptor, verify that the source remains part of the PK exactly once and that relation loading uses the source value.
- For a string-based `ObjectField` whose target uses a shared `OBJECT_KEY`, verify that its explicit discriminator resolves the intended related class, including any expected tuple fallback.
- Verify local assignment, `has_changes`, `reset_field`, `field(...).reset()`, `reset_changes`, `save`, and `refresh`.
- For `DictField`, verify in-place mutation followed by explicit `save(update_fields=[...])`, and verify that parameterless `save()` does not treat it as a local assignment.
- When response methods use different key casing, verify normalization occurs before PK extraction and leaves already canonical Bitrix codes unchanged.
- Verify partial missing fields reload once and complete missing optional fields return `None` without repeated requests.
- For composite keys, verify direct construction, raw response conversion, hashing/equality, exact `to_bitrix()` keys, and every allowed missing or nullable component.
- For a shared `OBJECT_KEY`, verify that every concrete discriminator resolves the correct class and that adapters pass the same value.
- Verify `required_class_params` are captured in metadata and appear in list/filter, add, update, and delete requests, while direct loaders pass them explicitly.
- Verify every non-default `request_name`, especially PK names used by default delete requests.
- For every entity-bound API method, verify that it obtains the scalar PK or required composite-PK components from `self.bitrix_pk`, forwards the remaining arguments and `timeout`, and returns the wrapper's adapted value.

### Managers

- Verify manager descriptor cloning and independent chained query state.
- Verify filter conversion and every exposed lookup.
- Verify top-level versus nested filter/order/add parameter shapes.
- Verify fixed class parameters cannot be changed through the concrete manager's public query surface.
- Verify PK filtering, including an empty ID iterable with no API request in the caller layer.
- Verify ordering, reverse, limit, start, count, first, last, exists, normal iteration, and fast iteration where supported.
- Verify `select` always includes PK fields and passes its effective list to the adapter.
- Verify `select_all()` requests every registered concrete Bitrix code while preserving existing nested selection state.
- Verify both no-select completeness modes: the default complete response and `_IS_COMPLETE_WITHOUT_SELECT = False` for reduced responses.
- Verify `select_related` for scalar, multiple, duplicate, nested, missing, and empty relations without N+1 requests. Verify that complete intermediate objects receive no implicit `select`, terminal ordinary fields are selected only on their owning manager, and `_IS_COMPLETE_WITHOUT_SELECT = False` adds only directly requested relation codes. A manager without public `select()` must fail only when its effective selection is non-empty.
- Verify unsupported operations fail before sending an API request.
- Verify every alternative returning method selects the correct scope wrapper, preserves prior query state, and is executable when called without optional parameters.
- Verify shared non-field request parameters use their chainable `with_*()` method and method-specific parameters are accepted only by the relevant manager method.
- Verify immediate command methods call the matching scope wrapper once, forward `MISSING` and iterables correctly, and return the adapted result.
- For object-backed field metadata, verify one `.values` request loads the complete collection, repeated lookups reuse `bitrix_objects`, and the cache key is `(metadata_object_key, metadata_discriminator)`.

### CRUD and batch

- Verify required add parameters and cross-field validation.
- Verify scalar, full-data, and one-key-wrapped add results when applicable.
- Verify command-style creation separately when the endpoint returns only `bool` and cannot construct an object.
- Verify object update/save synchronization only after a truthy API result.
- Verify count-returning deletion maps zero to `False` and a positive count to `True`, with every composite PK component mapped or omitted according to the wrapper contract.
- Verify file updates force authoritative metadata reload.
- Verify empty batch add/update/delete paths make no API request.
- Verify caller keys or sequence indexes are preserved for batch add errors.
- Verify `add_many()` accepts the same per-item field dictionary contract as `add()`, including every supported endpoint-specific creation parameter.
- Verify batch write results are mapped back to object instances.

### Static checks

- Run the project's supported formatter/linter, type checker, compilation check, and tests.
- Confirm that every function declaration and call follows the parameter-count formatting rule, including correct handling of `self`, `cls`, `*`, and `/`.
- Check completion and assignment diagnostics in the supported PyCharm and VS Code/Pylance versions for generic descriptors and managers.
- Confirm no generated method advertises an API capability the underlying scope does not provide.
- Confirm every stable compound raw result has a public `TypedDict`, the first request generic names that type, and any nested values adapter uses the exact wrapper key.

## 17. Common incorrect implementations

Do not:

- derive field flags from a similarly named entity;
- expose a raw Bitrix24 response field through an ad hoc `@property` that reads `bitrix_data` instead of declaring a field descriptor;
- treat absence from a partial response as `None`;
- define an enum or named `Literal` type outside `b24pysdk.constants`;
- omit the explicit generic parameter from `EnumField`, `FileField`, `ObjectField`, or `BitrixSchemaField`;
- create an inline source descriptor inside `ObjectField`;
- declare a discriminator-dependent `ObjectField` on a base class that cannot yet identify the related registry variant;
- expect `ObjectField` to derive a discriminator from its owner instead of passing the actual value explicitly;
- expose raw related IDs only when a stable related object exists and `select_related()` is supportable;
- use `None` as the omission sentinel in add/update signatures;
- annotate every omittable parameter as `Optional` even when explicit `None` is invalid;
- mark every non-PK field as read-only merely because the object exposes no `update()`/`save()` methods;
- mark add-only fields as read-only;
- update a server-owned or non-updatable field through public methods;
- require callers to repeat a scalar PK or composite-PK component in an object method that already has the same value in `self.bitrix_pk`;
- duplicate scope-wrapper serialization or call the raw REST transport from an object-specific API method;
- issue one API request per related object or per PK;
- expose the standard `from_pks()` for a composite key;
- assume a composite-key dataclass default is applied when metadata supplies an explicit `None` for a missing raw component;
- use ordinary `_add()` when the endpoint returns only a success flag and no PK;
- use ordinary `_delete()` when the endpoint returns an adapted removal count;
- mutate manager query state or caller-owned parameter mappings in place;
- pass a one-shot `select` generator separately to request construction and the adapter;
- assume every no-`select` response is complete;
- repeat a class-wide fixed API parameter in every CRUD method instead of declaring `get_required_class_params()`;
- model a fixed class discriminator parameter as part of `bitrix_pk` or as an ordinary mutable field solely to make requests work;
- rely on the generated request name when a wrapper uses a different Python parameter name;
- override generic CRUD builders only to append fixed class parameters already handled by metadata;
- synthesize an implicit ID-only select for the adapter instead of declaring `_IS_COMPLETE_WITHOUT_SELECT = False` on the object;
- normalize entity-specific response key casing inside the general object adapter instead of the object's `_normalize_bitrix_data()` hook;
- defensively copy a loaded `DictField` mapping when the entity supports explicit `save(update_fields=[...])` for in-place changes;
- override `_add_select_param()` to reinterpret an unrelated top-level `params` dictionary;
- expose `select`, `start`, ordering, fast mode, CRUD, or field metadata merely because the base class contains helpers;
- cache portal-specific metadata globally across clients;
- key client metadata caches by a Python class instead of `(OBJECT_KEY, get_discriminator())`;
- store adapted field objects in `bitrix_fields` or key them by the consumer object's identity instead of the metadata object's identity;
- fetch object-backed field metadata one field at a time instead of caching the complete `.values` result;
- annotate a descriptor class attribute as though it were only its instance value;
- split a function declaration or call with only one or two parameters/arguments across several lines, or keep three or more on one line;
- create a field manager whose `list()` result is not keyed by Bitrix24 field code;
- model endpoint-only request controls as object fields or ordinary filters;
- switch an alternative API wrapper without making a parameterless manager method executable;
- implement queue/package commands through object CRUD helpers or per-object loops;
- leave a stable compound result annotated as `JSONDict` when its keys can be described by a `TypedDict`;
- expose `add_many()` when its per-item dictionaries cannot express the same supported creation options as `add()`;
- rewrite unrelated scope-wrapper logic when only its raw result annotation needs to change.

## 18. Final acceptance rule

A generated object is complete only when all four layers agree:

1. Field descriptors accurately model raw and public values.
2. The object accurately models identity and lifecycle operations.
3. Managers expose only valid typed query and write operations.
4. Scope adapters construct the registered object with the correct response shape and data-completeness state.

If any layer requires guessing, stop and verify the endpoint contract or real response before generating code.
