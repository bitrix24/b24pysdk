## Integration scope tests

### 1. Location and structure

- Place all scope integration tests in `tests/integration/scopes/`.
- For each scope and its nested entities create separate files/directories:
  - If the scope **contains nested entities** (e.g. `bitrix_client.event.offline`), create a directory named after the **parent scope** and place test files for each nested entity inside:  
    → `tests/integration/scopes/event/test_offline.py`
  - If the scope **has no nested entities** and methods are called directly (e.g. `bitrix_client.feature.get()`), create a single test file directly under `scopes/`:  
    → `tests/integration/scopes/test_feature.py`
- For multi‑level scopes mirror the SDK module structure and REST method hierarchy.  
Example:  
REST method: `crm.lead.add`  
Test: `tests/integration/scopes/crm/test_lead.py::test_add`  
Test function name (`test_add`) must match the API method name (`add`).

---

### 2. Pytest markers

#### 2.1 File‑level markers

At the top of every scope test file set `pytestmark` with the common markers:

```python
pytestmark = [
    pytest.mark.integration,
    pytest.mark.<scope_name>,
]
```

Use the scope name from the SDK, e.g. `events`, `server`, `feature`, `crm`, etc.

**For nested scopes**, include both parent and child scope markers:

```python
pytestmark = [
    pytest.mark.integration,
    pytest.mark.user,           # parent scope
    pytest.mark.user_userfield, # nested scope
]
```

#### 2.2 Registering new markers

Register any new markers (including new scopes) in `pyproject.toml` under `tool.pytest.ini_options`:

```toml
[tool.pytest.ini_options]
markers = [
    "feature: mark a test as related to feature operations",
    "server: mark a test as related to server operations",
]
```

#### 2.3 `@pytest.mark.oauth_only`

Use `@pytest.mark.oauth_only` on tests that must run **only with OAuth** and are not supported for webhook auth:

```python
@pytest.mark.oauth_only
def test_events(bitrix_client: Client):
    ...
```

---

## 3. Writing a test for an API method

### 3.1 Base checks (required)

Use the `bitrix_client` fixture in all integration tests:

```python
from b24pysdk import Client

def test_feature_get(bitrix_client: Client):
    bitrix_response = bitrix_client.feature.get(code=B24PySDK_FEATURE_CODE).response
```

Always assert that the response is a Bitrix API response type:

```python
from b24pysdk.bitrix_api.responses import BitrixAPIResponse

bitrix_response = bitrix_client.feature.get(code=B24PySDK_FEATURE_CODE).response
assert isinstance(bitrix_response, BitrixAPIResponse)
```

Check the result type and structure:

```python
from typing import cast

result = cast(dict, bitrix_response.result)
assert isinstance(result, dict), "Method 'get' result should be a dict"
```

**Additional required checks:**
- For methods returning IDs, verify the ID is positive
- For methods returning booleans, verify the value is `True`

Constants:
- Place all local constants at the top of the file, after imports and `pytestmark`
- Use `UPPER_SNAKE_CASE` with a leading underscore
- **Add type hints**
- Use project constants from `...constants` module when available
- Name constants similarly to the parameters they are passed to. If it's a text parameter that you came up with yourself, add the `SDK_NAME` tag at the beginning, for example: `_NAME: Text = f"{SDK_NAME} DEPARTMENT NAME"`

Example:

```python
from typing import Text, Tuple
from ...constants import SDK_NAME, HEAD_DEPARTMENT_ID, BITRIX_PORTAL_OWNER_ID

_FIELDS: Tuple[Text, ...] = ("ID", "NAME", "SORT", "PARENT", "UF_HEAD")
_NAME: Text = f"{SDK_NAME} DEPARTMENT NAME"
_SORT: int = 123
```

### 3.2 Structure checks

**Important**: In GET methods or any methods that retrieve objects created from local constants, always verify that the fields match the expected constant values.

Presence of fields:

```python
_FIELDS = ("ID", "ADMIN", "NAME", "LAST_NAME", "PERSONAL_GENDER", "TIME_ZONE", "PERSONAL_PHOTO")

def test_profile(bitrix_client: Client):
    ...
    for field in _FIELDS:
        assert field in user_profile, f"Field '{field}' should be present"
```

Concrete values with proper type handling:

```python
def test_department_get(bitrix_client: Client, cache: Cache):
    """"""

    department_id = cache.get("department_id", None)
    assert isinstance(department_id, int), "Department ID should be cached"

    bitrix_response = bitrix_client.department.get(bitrix_id=department_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)

    departments = cast(list, bitrix_response.result)

    assert len(departments) == 1, "Expected one department to be returned"
    department = departments[0]

    assert isinstance(department, dict)

    assert department.get("ID") == str(department_id), "Department ID does not match"
    assert department.get("NAME") == _NAME, "Department NAME does not match"
    assert department.get("PARENT") == str(HEAD_DEPARTMENT_ID), "Department PARENT does not match"
    assert department.get("UF_HEAD") == str(BITRIX_PORTAL_OWNER_ID), "Department UF_HEAD does not match"
    assert department.get("SORT") == _SORT, "Department SORT does not match"
```

Nested structures:

```python
assert isinstance(user_userfield.get("SETTINGS"), dict), "User userfield SETTINGS is not a dictionary"

user_userfield_settings = cast(dict, user_userfield["SETTINGS"])
assert user_userfield_settings.get("DEFAULT_VALUE") == _SETTINGS_DEFAULT_VALUE
```

### 3.3 Methods returning lists

1. Regular list method test using `BitrixAPIResponse`:

```python
def test_department_get(bitrix_client: Client):
    bitrix_response = bitrix_client.department.get(bitrix_id=department_id).response
    
    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)
    
    departments = cast(list, bitrix_response.result)
    assert len(departments) == 1, "Expected one department to be returned"
```

If the method supports a prefix filter, call it with the filter and check the prefix:

```python
def test_placement_list(bitrix_client: Client):
    bitrix_response = bitrix_client.placement.list(scope=_SCOPE).response
    ...
    for placement in placements:
        assert isinstance(placement, str), "Placement should be a string"
        assert placement.startswith(f"{_SCOPE.upper()}_"), f"Placement should be prefixed with {_SCOPE.upper()}_"
```

2. `as_list` test:
   - Call `.as_list()` and assert `BitrixAPIListResponse`
   - Result should be a `list`
   - Include dependency markers for tests that depend on data creation

```python
@pytest.mark.dependency(name="test_user_get_as_list", depends=["test_user_add"])
def test_user_get_as_list(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.user.get().as_list().response

    assert isinstance(bitrix_response, BitrixAPIListResponse)
    assert isinstance(bitrix_response.result, list)

    users = cast(list, bitrix_response.result)

    assert len(users) >= 1, "Expected at least one user to be returned"

    for user in users:
        assert isinstance(user, dict)
```

3. `as_list_fast` test for ID-ordered lists:
   - Use `.as_list_fast(descending=...)`
   - Assert `BitrixAPIListFastResponse` type
   - Result is a `Generator`, not a `list`

```python
def test_user_get_as_list_fast(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.user.get().as_list_fast(descending=True).response

    assert isinstance(bitrix_response, BitrixAPIListFastResponse)
    assert isinstance(bitrix_response.result, Generator)

    users = cast(JSONDictGenerator, bitrix_response.result)

    last_user_id = None

    for user in users:
        assert isinstance(user, dict)
        assert "ID" in user

        user_id = int(user["ID"])

        if last_user_id is None:
            last_user_id = user_id
        else:
            assert last_user_id > user_id
            last_user_id = user_id
```

### 3.4 Dependent tests with cache

Use dependency markers and the `cache` fixture when tests must reuse values from previous tests:

```python
@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_department_add")
def test_department_add(bitrix_client: Client, cache: Cache):
    """Test department.add method."""
    
    bitrix_response = bitrix_client.department.add(
        name=_NAME,
        parent=HEAD_DEPARTMENT_ID,
    ).response
    
    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, int)
    
    department_id = cast(int, bitrix_response.result)
    assert department_id > 0, "Department creation should return a positive ID"
    
    cache.set("department_id", department_id)

@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_department_update", depends=["test_department_add"])
def test_department_update(bitrix_client: Client, cache: Cache):
    """Test department.update method."""
    
    department_id = cache.get("department_id", None)
    assert isinstance(department_id, int), "Department ID should be cached"
    
    bitrix_response = bitrix_client.department.update(
        bitrix_id=department_id,
        sort=_SORT,
    ).response
    
    assert isinstance(bitrix_response, BitrixAPIResponse)
    is_updated = cast(bool, bitrix_response.result)
    assert is_updated is True, "Department update should return True"

@pytest.mark.oauth_only  
@pytest.mark.dependency(name="test_department_delete", depends=["test_department_get_as_list_fast"])
def test_department_delete(bitrix_client: Client, cache: Cache):
    """Test department.delete method."""
    
    department_id = cache.get("department_id", None)
    assert isinstance(department_id, int), "Department ID should be cached"
    
    bitrix_response = bitrix_client.department.delete(bitrix_id=department_id).response
    
    assert isinstance(bitrix_response, BitrixAPIResponse)
    is_deleted = cast(bool, bitrix_response.result)
    assert is_deleted is True, "Department deletion should return True"
```

---

## 4. Generating unique test data

Generate unique test data only when you need to reference objects by that field to prevent conflicts during parallel test execution. 
```python
from b24pysdk import Config

# Unique email based on timestamp
email: Text = f"{int(Config().get_local_datetime().timestamp() * (10 ** 6))}@pysdktest.com"

# Unique field name
field_name = f"UF_USR_{SDK_NAME.upper()}_{int(Config().get_local_datetime().timestamp() * (10 ** 6))}"
```

---

## 5. Test documentation and structure

### 5.1 Docstrings

Include blank docstrings for all test functions:

```python
def test_department_fields(bitrix_client: Client):
    """"""
```

### 5.2 Test order and dependencies

Follow this logical order for CRUD tests:
1. `test_fields()` - if available (no dependencies)
2. `test_add()` - creates entity, stores ID in cache
3. `test_update()` - depends on `test_add`, modifies entity
4. `test_get()`/`test_list()` - depends on `test_update`, verifies changes
5. `test_delete()` - depends on all previous, cleans up

**Important:** Always explicitly declare dependencies in the `@pytest.mark.dependency` decorator, even if tests are written in correct order in the file. Example: `@pytest.mark.dependency(name="test_department_get", depends=["test_department_add"])`

---

## 6. Common assertions and validations

### 6.1 Response type assertions

```python
# For regular responses
assert isinstance(bitrix_response, BitrixAPIResponse)

# For as_list() responses  
assert isinstance(bitrix_response, BitrixAPIListResponse)

# For as_list_fast() responses
assert isinstance(bitrix_response, BitrixAPIListFastResponse)
```

### 6.2 Result type assertions (before cast)

```python
assert isinstance(bitrix_response.result, dict)  # before cast(dict, ...)
assert isinstance(bitrix_response.result, list)  # before cast(list, ...)
assert isinstance(bitrix_response.result, int)   # before cast(int, ...)
assert isinstance(bitrix_response.result, bool)  # before cast(bool, ...)
```

### 6.3 Value assertions

```python
# For IDs returned from add()
entity_id = cast(int, bitrix_response.result)
assert entity_id > 0, "Entity creation should return a positive ID"

# For boolean results from update/delete
is_success = cast(bool, bitrix_response.result)
assert is_success is True, "Operation should return True"

# For list results
items = cast(list, bitrix_response.result)
assert len(items) >= 1, "Expected at least one item to be returned"
```

### 6.4 Cache validation

```python
entity_id = cache.get("entity_id", None)
assert isinstance(entity_id, int), "Entity ID should be cached and be an integer"
```

---

## 7. Complete test example template

```python
from datetime import date, datetime
from typing import Generator, List, Text, Tuple, cast

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk import Client, Config
from b24pysdk.bitrix_api.responses import BitrixAPIListFastResponse, BitrixAPIListResponse, BitrixAPIResponse
from b24pysdk.constants.user import PersonalGender
from b24pysdk.utils.types import JSONDictGenerator

from ....constants import HEAD_DEPARTMENT_ID, SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.user,
]

_FIELDS: Tuple[Text, ...] = ("ID", "XML_ID", "ACTIVE", "NAME", "LAST_NAME", "EMAIL", "LAST_LOGIN", "DATE_REGISTER", "TIME_ZONE", "IS_ONLINE", "TIMESTAMP_X",
                             "LAST_ACTIVITY_DATE", "PERSONAL_GENDER", "PERSONAL_BIRTHDAY", "UF_EMPLOYMENT_DATE", "UF_DEPARTMENT")

_NAME: Text = "Test"
_LAST_NAME: Text = SDK_NAME
_UF_DEPARTMENT_ID_LIST: List = [HEAD_DEPARTMENT_ID]
_ACTIVE: bool = False
_PERSONAL_GENDER: PersonalGender = PersonalGender.MALE
_PERSONAL_PROFESSION: Text = f"{SDK_NAME}-Developer"
_PERSONAL_BIRTHDAY: date = Config().get_local_date()

_ACCESS: List[Text] = ["AU", "G2"]


def test_user_fields(bitrix_client: Client):
    """Test retrieving user fields and validating the structure."""

    bitrix_response = bitrix_client.user.fields().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    fields = cast(dict, bitrix_response.result)

    for field in _FIELDS:
        assert field in fields, f"Field '{field}' should be present"
        assert isinstance(fields[field], str), f"Field '{field}' should be a string"


@pytest.mark.dependency(name="test_user_add")
def test_user_add(bitrix_client: Client, cache: Cache):
    """Test addition of a new user and validate successful creation."""

    email: Text = f"{int(Config().get_local_datetime().timestamp() * (10 ** 6))}@pysdktest.com"

    bitrix_response = bitrix_client.user.add(
        fields={
            "NAME": _NAME,
            "LAST_NAME": _LAST_NAME,
            "EMAIL": email,
            "UF_DEPARTMENT": _UF_DEPARTMENT_ID_LIST,
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, int)

    user_id = cast(int, bitrix_response.result)

    assert user_id > 0, "The result should be a positive integer representing the user ID"

    cache.set("user_id", user_id)
    cache.set("user_email", email)


@pytest.mark.dependency(name="test_user_get", depends=["test_user_add"])
def test_user_get(bitrix_client: Client, cache: Cache):
    """Test retrieving a user by ID."""

    user_id = cache.get("user_id", None)
    assert isinstance(user_id, int), "User ID should be cached after addition"

    user_email = cache.get("user_email", None)
    assert isinstance(user_email, str), "User email should be cached after addition"

    bitrix_response = bitrix_client.user.get(
        filter={
            "ID": user_id,
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)

    users = cast(list, bitrix_response.result)

    assert len(users) == 1, "Expected one user to be returned"
    user = users[0]

    assert isinstance(user, dict)
    assert user.get("ID") == str(user_id), "Returned user ID does not match expected"
    assert user.get("NAME") == _NAME, "Name does not match"
    assert user.get("LAST_NAME") == _LAST_NAME, "Last name does not match"
    assert user.get("EMAIL") == user_email, "Email does not match"
    assert user.get("UF_DEPARTMENT") == _UF_DEPARTMENT_ID_LIST, "Department does not match"


@pytest.mark.dependency(name="test_user_get_as_list", depends=["test_user_add"])
def test_user_get_as_list(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.user.get().as_list().response

    assert isinstance(bitrix_response, BitrixAPIListResponse)
    assert isinstance(bitrix_response.result, list)

    users = cast(list, bitrix_response.result)

    assert len(users) >= 1, "Expected at least one user to be returned"

    for user in users:
        assert isinstance(user, dict)


@pytest.mark.dependency(name="test_user_get_as_list_fast", depends=["test_user_add"])
def test_user_get_as_list_fast(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.user.get().as_list_fast(descending=True).response

    assert isinstance(bitrix_response, BitrixAPIListFastResponse)
    assert isinstance(bitrix_response.result, Generator)

    users = cast(JSONDictGenerator, bitrix_response.result)

    last_user_id = None

    for user in users:
        assert isinstance(user, dict)
        assert "ID" in user

        user_id = int(user["ID"])

        if last_user_id is None:
            last_user_id = user_id
        else:
            assert last_user_id > user_id
            last_user_id = user_id


@pytest.mark.dependency(name="test_user_update", depends=["test_user_add"])
def test_user_update(bitrix_client: Client, cache: Cache):
    """Test updating an existing user's attributes."""

    user_id = cache.get("user_id", None)
    assert isinstance(user_id, int), "User ID should be cached"

    bitrix_response = bitrix_client.user.update(
        fields={
            "ID": user_id,
            "ACTIVE": _ACTIVE,
            "WORK_POSITION": f"{_PERSONAL_PROFESSION} {user_id}",
            "PERSONAL_GENDER": _PERSONAL_GENDER,
            "PERSONAL_PROFESSION": _PERSONAL_PROFESSION,
            "PERSONAL_BIRTHDAY": _PERSONAL_BIRTHDAY.isoformat(),
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_updated = cast(bool, bitrix_response.result)

    assert is_updated is True, "User update should return True"


@pytest.mark.dependency(name="test_user_search", depends=["test_user_update"])
def test_user_search(bitrix_client: Client, cache: Cache):
    """Test searching for users by a given criteria."""

    user_id = cache.get("user_id", None)
    assert isinstance(user_id, int), "User ID should be cached"

    user_email = cache.get("user_email", None)
    assert isinstance(user_email, str), "User email should be cached after addition"

    bitrix_response = bitrix_client.user.search(
        filter={
            "FIND": f"{_PERSONAL_PROFESSION} {user_id}",
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)

    users = cast(list, bitrix_response.result)

    assert len(users) == 1, "Expected one user to be returned"

    user = users[0]

    assert isinstance(user, dict)

    assert user.get("ID") == str(user_id), "Returned user ID does not match expected"
    assert user.get("NAME") == _NAME, "Name does not match"
    assert user.get("LAST_NAME") == _LAST_NAME, "Last name does not match"
    assert user.get("EMAIL") == user_email, "Email does not match"
    assert user.get("UF_DEPARTMENT") == _UF_DEPARTMENT_ID_LIST, "Department does not match"
    assert user.get("ACTIVE") is _ACTIVE, "Activation does not match after update"
    assert user.get("WORK_POSITION") == f"{_PERSONAL_PROFESSION} {user_id}", "User's work position does not match after update"
    assert user.get("PERSONAL_GENDER") == _PERSONAL_GENDER, "User's personal gender does not match after update"
    assert user.get("PERSONAL_PROFESSION") == _PERSONAL_PROFESSION, "User's personal profession does not match after update"
    assert (user.get("PERSONAL_BIRTHDAY") and datetime.fromisoformat(user["PERSONAL_BIRTHDAY"]).date()) == _PERSONAL_BIRTHDAY, "User's personal birthday does not match after update"


@pytest.mark.dependency(name="test_user_search", depends=["test_user_update"])
def test_user_search_as_list(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.user.search().as_list().response

    assert isinstance(bitrix_response, BitrixAPIListResponse)
    assert isinstance(bitrix_response.result, list)

    users = cast(list, bitrix_response.result)

    assert len(users) >= 1, "Expected at least one user to be returned"

    for user in users:
        assert isinstance(user, dict)


@pytest.mark.dependency(name="test_user_search", depends=["test_user_update"])
def test_user_search_as_list_fast(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.user.search().as_list_fast(descending=True).response

    assert isinstance(bitrix_response, BitrixAPIListFastResponse)
    assert isinstance(bitrix_response.result, Generator)

    users = cast(JSONDictGenerator, bitrix_response.result)

    last_user_id = None

    for user in users:
        assert isinstance(user, dict)
        assert "ID" in user

        user_id = int(user["ID"])

        if last_user_id is None:
            last_user_id = user_id
        else:
            assert last_user_id > user_id
            last_user_id = user_id


def test_user_current(bitrix_client: Client):
    """Test retrieving details of the current user."""

    bitrix_response = bitrix_client.user.current().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    user = cast(dict, bitrix_response.result)

    for field in _FIELDS:
        assert field in user, f"Field '{field}' should be present"
        assert isinstance(user[field], (bool, str, list)), f"Field '{field}' should be a bool, string or list"


def test_user_admin(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.user.admin().response
    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_admin = cast(bool, bitrix_response.result)
    assert is_admin is True, "User admin should return True"


def test_user_access(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.user.access(access=_ACCESS).response
    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_available = cast(bool, bitrix_response.result)
    assert is_available is True, "User access should return True"
```
