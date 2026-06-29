# API Result Classes Creation Guide

This guide describes how to decide whether a Bitrix24 REST API method needs a schema class, a standard Python conversion, a future object class, or no class at all.

It is intended for SDK contributors who add or update API scopes, result adapters, schemas, and future object-layer classes.

## 1. Goal

For each Bitrix24 REST API method, the SDK should clearly define how the method result is exposed.

The SDK keeps two levels of access:

```python
request.result  # raw Bitrix24 API result
request.value   # adapted single value
request.values  # adapted list / generator of values
```

`request.result` should stay as close as possible to the original Bitrix24 API payload.

`request.value` and `request.values` are used for typed SDK results.

## 2. Result Categories

### Type 1 — Simple result, no class required

Use this type when the API result does not require a custom class.

Examples:

```python
True
123
"success"
["crm", "user", "task"]
{"CODE": "Title"}
```

This also includes responses shaped as **one key wrapping one scalar value**:

```python
{"id": 123}
{"count": 5}
{"result": True}
```

Do not create schema classes for such responses. Use a `lambda` adapter instead:

```python
return self._make_bitrix_api_request(
    api_wrapper=self.some_method,
    params=params,
    timeout=timeout,
    bitrix_api_request_type=BitrixAPIValueRequest,
    result_adapter=lambda result: result["id"],
)
```

Examples:

```python
event.unbind -> lambda result: result["count"]
placement.unbind -> lambda result: result["count"]
crm.duplicate.volatiletype.register -> lambda result: result["id"]
```

If the API returns plain `bool`, `int`, `str`, `float`, `list[str]`, or `dict[str, str]`, no class is required.

---

### Type 2 — Conversion to a standard Python type

Use this type when the API returns a simple raw value, but the SDK should expose a more convenient standard Python type.

Example:

```python
server.time
```

Bitrix24 returns a datetime string, while the SDK should expose `datetime`.

```python
return self._make_bitrix_api_request(
    api_wrapper=self.time,
    params=params,
    timeout=timeout,
    bitrix_api_request_type=BitrixAPIValueRequest,
    result_adapter=lambda result: datetime_from_bitrix(result, is_required=True),
)
```

Typical conversions:

```python
str -> datetime
str -> date
int -> timedelta
str/int -> Enum
```

If no custom class is needed, do not create a schema.

---

### Type 3 — Schema class

Use a schema class when the API returns a structured object without lifecycle behavior.

A schema is a DTO: data fields plus `from_bitrix()` and `to_bitrix()`.

A schema must not contain business methods such as:

```python
save()
delete()
refresh()
update()
```

Example raw result:

```python
{
    "ID": 1,
    "NAME": "Roman",
    "LAST_NAME": "Ldokov"
}
```

Schema example:

```python
class ProfileData(TypedDict):
    ID: int
    NAME: Text
    LAST_NAME: Text


@dataclass(**frozen_dataclass_kwargs())
class Profile(BaseSchema[ProfileData]):
    bitrix_id: int
    name: Text
    last_name: Text

    @classmethod
    def from_bitrix(cls, bitrix_data: ProfileData, /) -> "Profile":
        return cls(
            bitrix_id=bitrix_data["ID"],
            name=bitrix_data["NAME"],
            last_name=bitrix_data["LAST_NAME"],
        )

    def to_bitrix(self) -> ProfileData:
        return {
            "ID": self.bitrix_id,
            "NAME": self.name,
            "LAST_NAME": self.last_name,
        }
```

Scope method example:

```python
return self._make_bitrix_api_request(
    api_wrapper=self.profile,
    params=params,
    timeout=timeout,
    bitrix_api_request_type=BitrixAPIValueRequest,
    result_adapter=Profile.from_bitrix,
)
```

---

### Type 4 — Object class

Use an object class for entities with lifecycle behavior.

An object is needed when the result represents a domain entity that may later support use-case methods in the SDK:

```python
deal.update(...)
deal.delete()
deal.refresh()
task.complete()
item.save()
```

Main rule:

> If an entity is retrieved through a list/retrieval method that has `select`, `order`, or `filter` parameters, the result belongs to the object layer.

Examples:

```python
crm.deal.list(select=..., order=..., filter=...)
crm.item.list(select=..., order=..., filter=...)
event.offline.list(filter=...)
event.offline.get(filter=...)
department.get(filter=...)
user.get(filter=...)
lists.element.get(filter=...)
entity.item.get(filter=...)
```

Even if the method name is not `list`, but rather `get`, `getchildren`, `search`, `tail`, or `instances`, it is still an object candidate when it has `filter`, `order`, or `select` and returns entities.

Until the `objects` module exists, such methods may temporarily use schemas, but they should be classified as **TYPE 4 / OBJECT** in the method classification table.

## 3. Rules for `fields` Methods

### Direct field map

If the API returns:

```python
{
    "TITLE": {
        "type": "string",
        "isRequired": False,
        "title": "Title"
    },
    "PHONE": {
        "type": "crm_multifield",
        "isMultiple": True,
        "title": "Phone"
    }
}
```

use `CRMFieldsDict`:

```python
BitrixAPIValueRequest[CRMFieldsData, CRMFieldsDict]
result_adapter=CRMFieldsDict.from_bitrix
```

The user receives:

```python
request.value["TITLE"].title
```

---

### Wrapped field map

If the API returns:

```python
{
    "fields": {
        "title": {...},
        "createdTime": {...}
    }
}
```

or:

```python
{
    "orderEntity": {
        "id": {...},
        "accountNumber": {...}
    }
}
```

a separate result class is not needed if there is a reusable `BaseSchemaDict` / `CRMFieldsDict` implementation with `_WRAPPER`.

Example:

```python
class CRMFieldsDict(BaseSchemaDict[CRMField, CRMFieldData]):
    _ITEM_SCHEMA = CRMField
    _WRAPPER = "fields"
```

For another wrapper:

```python
class OrderentityFieldsDict(CRMFieldsDict):
    _WRAPPER = "orderEntity"
```

Then map methods like this:

```python
crm.item.fields -> CRMFieldsDict
crm.category.fields -> CRMFieldsDict
crm.type.fields -> CRMFieldsDict
crm.item.productrow.fields -> CRMFieldsDict
crm.orderentity.getFields -> OrderentityFieldsDict
```

The user should still get a direct field dictionary:

```python
request.value["title"]
```

not:

```python
request.value.fields["title"]
```

---

### Simple code-to-title map

If a method returns:

```python
{
    "CODE_1": "Title 1",
    "CODE_2": "Title 2"
}
```

this is **Type 1** and no class is required:

```python
Dict[Text, Text]
```

## 4. When to Create `TypedDict`

Every schema class should have a raw Bitrix data type.

Example:

```python
class CRMFieldData(TypedDict):
    type: Text
    isRequired: bool
    isReadOnly: bool
    isImmutable: bool
    isMultiple: bool
    isDynamic: bool
    title: Text
```

Use a separate `TypedDict(total=False)` for optional fields:

```python
class _CRMFieldOptionalData(TypedDict, total=False):
    items: CRMFieldItemsData
    settings: JSONDict
    listLabel: Text
```

Then extend it:

```python
class CRMFieldData(_CRMFieldOptionalData):
    type: Text
    isRequired: bool
    isReadOnly: bool
    isImmutable: bool
    isMultiple: bool
    isDynamic: bool
    title: Text
```

## 5. Naming Conventions

### Raw data type

```python
ProfileData
CRMFieldData
CRMFieldsData
EventOfflineData
```

### Schema class

```python
Profile
CRMField
EventOffline
```

Naming must not make a simple DTO look like a lifecycle entity.

If the schema name is a general shared CRM concept, prefix it with `CRM`:

```python
CRMStatus
CRMField
CRMFieldsDict
```

If the name already clearly belongs to CRM or is a domain entity name such as
`Deal`, `Activity`, `ActivityBinding`, `ActivityBadge`, or `AutomationTrigger`,
do not add a schema class for it just because a method returns that shape.
These names are reserved for future object/lifecycle classes.

For entities that have, or naturally may have, lifecycle operations such as
`add`, `update`, `delete`, `move`, `bind`, `unbind`, `get`, or `list`, do not
create schema classes in `b24pysdk.schemas`. Start with the simplest safe
typing in the scope method return type, for example:

```python
BitrixAPIRequest[JSONList]
BitrixAPIRequest[JSONDict]
```

Use `JSONList` for arrays of JSON objects instead of spelling
`List[JSONDict]` directly. Keep `List[...]` only for primitive or explicitly
non-JSON-object lists, for example `List[int]` or `List[Text]`.

Only add schema classes for auxiliary DTOs, metadata, fields, dictionaries,
settings, and read-only helper results that are not expected to become SDK
objects with lifecycle behavior.

### Dictionary schema

```python
CRMFieldsDict
AccessNamesDict
```

### List item schema

If the method returns a list of objects, name the class in singular form:

```python
CRMDuplicateVolatileTypeField
```

The method should return:

```python
BitrixAPIValuesRequest[..., CRMDuplicateVolatileTypeField]
```

## 6. How to Connect Schemas in Scope Methods

### Single schema object

```python
def get(...) -> BitrixAPIValueRequest[SomeData, SomeSchema]:
    return self._make_bitrix_api_request(
        api_wrapper=self.get,
        params=params,
        timeout=timeout,
        bitrix_api_request_type=BitrixAPIValueRequest,
        result_adapter=SomeSchema.from_bitrix,
    )
```

### List of schema objects

```python
def list(...) -> BitrixAPIValuesRequest[SomeData, SomeSchema]:
    return self._make_bitrix_api_request(
        api_wrapper=self.list,
        params=params,
        timeout=timeout,
        bitrix_api_request_type=BitrixAPIValuesRequest,
        result_adapter=SomeSchema.from_bitrix,
    )
```

### Simple scalar unwrap

```python
def add(...) -> BitrixAPIValueRequest[IDResultData, int]:
    return self._make_bitrix_api_request(
        api_wrapper=self.add,
        params=params,
        timeout=timeout,
        bitrix_api_request_type=BitrixAPIValueRequest,
        result_adapter=lambda result: result["id"],
    )
```

### Standard Python conversion

```python
def time(...) -> BitrixAPIValueRequest[Text, datetime]:
    return self._make_bitrix_api_request(
        api_wrapper=self.time,
        params=params,
        timeout=timeout,
        bitrix_api_request_type=BitrixAPIValueRequest,
        result_adapter=lambda result: datetime_from_bitrix(result, is_required=True),
    )
```

## 7. Choosing Between Schema and Object

### Use Schema when the result is:

```text
- a dictionary/reference result;
- a field description;
- settings;
- metadata;
- operation result data;
- a DTO without lifecycle;
- an object that the SDK should not update/delete directly.
```

Examples:

```python
profile
method.get
feature.get
crm.company.fields
crm.item.fields
crm.duplicate.volatileType.fields
```

### Use Object when the result is:

```text
- a Bitrix24 business entity;
- retrieved through list/get/search with filter/order/select;
- related to add/update/delete/get/list lifecycle methods;
- expected to support SDK use-case behavior.
```

Examples:

```python
crm.deal
crm.contact
crm.company
crm.item
task.item
department
user
event.offline
lists.element
entity.item
```

## 8. Special Rule for Single-Key Scalar Wrappers

Do not create a schema class for:

```python
{"id": 123}
{"count": 10}
{"success": True}
```

Even though the result is a dictionary, it is only wrapping a scalar value.

Correct:

```python
result_adapter=lambda result: result["id"]
```

Incorrect:

```python
class IDResult(BaseSchema[IDResultData]):
    ...
```

Exception: if the single key contains a structured value:

```python
{"fields": {...}}
{"item": {...}}
{"user": {...}}
{"result": {"id": 1, "name": "..."}}
```

then the result should be handled as schema or object.

## 9. Scope Typing Workflow

Type API results scope by scope, moving from simple results to complex results.

Do not start with arbitrary methods from different scopes. A whole scope must be inventoried first, so similar methods are typed consistently.

For each scope, prepare a method table with:

- method name;
- current SDK return type;
- documented raw `result`;
- Bitrix MCP raw `result`;
- real raw API `result`, when safe to call;
- result category;
- planned SDK exposure: `.result`, `.value`, `.values`, or future object;
- verification status.

Process each scope in this order:

1. Type simple raw results: `bool`, `int`, `str`, `float`, `None`, primitive lists, primitive dictionaries.
2. Type scalar wrappers such as `{"id": int}` and `{"count": int}` with `BitrixAPIValueRequest` and a `lambda` adapter.
3. Type standard conversions such as Bitrix datetime strings, dates, booleans, and enum-like values.
4. Type direct and wrapped field maps through `BaseSchemaDict` implementations.
5. Type DTO-like read-only structured objects through `BaseSchema` or `BaseListableSchema`.
6. Mark lifecycle entities as future object-layer candidates before adding temporary schemas.

This order keeps the implementation small and prevents generating schema classes for results that should stay primitive or become objects later.

## 10. Checklist for a New Method

Before creating a result class, answer these questions:

1. What does `result` look like in the official Bitrix24 documentation?
2. What does `result` look like in the Bitrix24 MCP method details?
3. What does `result` look like in a real API response from a test portal?
4. Is the real API response identical to the documented result shape?
5. Is it a scalar, primitive list, or primitive dictionary?
6. Is it a single-key scalar wrapper such as `{"id": int}`?
7. Does it need conversion to a standard Python type?
8. Is it a structured DTO without lifecycle behavior?
9. Is it an entity with `filter`, `order`, or `select` retrieval methods?
10. Does the entity have `add`, `update`, `delete`, `get`, or `list` methods?
11. Is it a `fields` method?
12. Is it a direct field map or a wrapped field map?
13. What should the user receive in `.value` or `.values`?

## 11. Result Shape Contract

Do not create or wire a schema from the method name, from similar methods, or from an incomplete documentation example.

Before adding `result_adapter`, `BitrixAPIValueRequest`, or `BitrixAPIValuesRequest`, define a strict result-shape contract for the method.

The contract must include:

- REST method name;
- official documentation source;
- Bitrix MCP method details result shape;
- real raw API `result` from a test portal, when the method can be safely executed;
- final raw result type used for `request.result`;
- final adapted type used for `request.value` or `request.values`;
- wrapper key, if the result is wrapped, for example `fields`, `items`, or `orderEntity`;
- adapter function or schema class;
- verification status.

Use this format while preparing a method:

```text
method: crm.some.method
documented_result: {"fields": {"FIELD": {...}}}
mcp_result: {"fields": {"FIELD": {...}}}
real_result: {"fields": {"FIELD": {...}}}
raw_result_type: Dict[Text, Dict[Text, CRMFieldData]]
value_type: CRMFieldsDict
wrapper: fields
adapter: CRMFieldsDict.from_bitrix
verified: yes
```

If the method cannot be safely executed on a test portal, set `verified: docs-only` and do not wire `.value` or `.values` unless the result shape is fully documented and unambiguous.

If the official documentation, Bitrix MCP details, and real API response disagree, use the real API response as the implementation source and document the mismatch in the contract before coding.

No raw result contract means no schema wiring.

## 12. Classification Algorithm

```text
1. If result is bool/int/str/float/list[str]/dict[str, str]:
   -> Type 1, no class.

2. If result is {"id": scalar} or {"count": scalar}:
   -> Type 1, no class, lambda unwrap.

3. If result is scalar but should become datetime/date/enum:
   -> Type 2, converter function.

4. If result is a field map:
   -> Type 3, CRMFieldsDict or another BaseSchemaDict.

5. If result is a structured dictionary without lifecycle:
   -> Type 3, BaseSchema.

6. If result is a list of structured dictionaries without lifecycle:
   -> Type 3, BaseListableSchema / BitrixAPIValuesRequest.

7. If the method returns business entities and has filter/order/select:
   -> Type 4, object.

8. If unsure between schema and object:
   - lifecycle and use-case methods -> object;
   - data/metadata only -> schema.
```

## 13. What to Test

For every method with a schema/object adapter, test not only `.result`, but also `.value` or `.values`.

Single schema example:

```python
response = client.profile()
assert response.result
assert response.value
assert isinstance(response.value, Profile)
```

Field map example:

```python
response = client.crm.company.fields()
assert response.result
assert response.value
assert isinstance(response.value, CRMFieldsDict)

first_field = next(iter(response.value.values()))
assert isinstance(first_field, CRMField)
```

List example:

```python
response = client.crm.duplicate.volatile_type.fields()
assert response.result
assert response.values

for item in response.values:
    assert isinstance(item, CRMDuplicateVolatileTypeField)
```

Scalar unwrap example:

```python
response = client.event.unbind(...)
assert isinstance(response.value, int)
```

## 14. Main Rule

Do not create classes just for the sake of having classes.

A class is needed only if it provides at least one of the following:

```text
1. Bitrix naming -> Python naming normalization;
2. nested data conversion;
3. future lifecycle / use-case behavior.
```

If the result is just `{"id": 123}` or `{"count": 5}`, use a `lambda`.
