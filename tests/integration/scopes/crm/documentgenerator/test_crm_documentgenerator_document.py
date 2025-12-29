from typing import Text, Tuple, cast

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk import Client
from b24pysdk.bitrix_api.responses import BitrixAPIListResponse, BitrixAPIResponse

from .....constants import SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.crm,
    pytest.mark.documentgenerator,
    pytest.mark.documentgenerator_document,
]

_DOCUMENT_ID: int = 9
_TEMPLATE_ID: int = 1
_ENTITY_TYPE_ID: int = 2
_ENTITY_ID: int = 5
_TITLE: Text = f"{SDK_NAME} Document"
_NUMBER: int = 1
_REGION: Text = "US"
_STAMPS_ENABLED: bool = True
_VALUES: dict = {"field1": "value1", "field2": "value2"}
_FILE_CONTENT: Text = "SGVsbG8gV29ybGQ="

_DOCUMENT_FIELDS: Tuple[Text, ...] = (
    "id",
    "title",
    "number",
    "createTime",
    "updateTime",
    "createdBy",
    "updatedBy",
    "stampsEnabled",
    "downloadUrl",
    "downloadUrlMachine",
    "publicUrl",
    "isTransformationError",
    "templateId",
    "entityTypeId",
    "entityId",
    "values",
)

_FILTER = {
    "entityTypeId": _ENTITY_TYPE_ID,
    "entityId": _ENTITY_ID,
}
_START: int = 0


def test_crm_documentgenerator_document_getfields(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.crm.documentgenerator.document.getfields(
        bitrix_id=_DOCUMENT_ID,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    fields = cast(dict, bitrix_response.result)

    assert len(fields) > 0, "Fields should not be empty"


@pytest.mark.dependency(name="test_crm_documentgenerator_document_add")
def test_crm_documentgenerator_document_add(bitrix_client: Client, cache: Cache):
    """"""

    bitrix_response = bitrix_client.crm.documentgenerator.document.add(
        template_id=_TEMPLATE_ID,
        entity_type_id=_ENTITY_TYPE_ID,
        entity_id=_ENTITY_ID,
        values=_VALUES,
        stamps_enabled=_STAMPS_ENABLED,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    response_dict = cast(dict, bitrix_response.result)
    assert "document" in response_dict, "Response should contain 'document' key"

    document = cast(dict, response_dict["document"])

    for field in _DOCUMENT_FIELDS:
        assert field in document, f"Field '{field}' should be present"

    document_id = int(document.get("id", 0))
    assert document_id > 0, "Document creation should return a positive ID"

    cache.set("created_document_id", document_id)


@pytest.mark.dependency(name="test_crm_documentgenerator_document_get", depends=["test_crm_documentgenerator_document_add"])
def test_crm_documentgenerator_document_get(bitrix_client: Client, cache: Cache):
    """"""

    document_id = cache.get("created_document_id", None)
    assert isinstance(document_id, int), "Created document ID should be cached"

    bitrix_response = bitrix_client.crm.documentgenerator.document.get(
        bitrix_id=document_id,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    response_dict = cast(dict, bitrix_response.result)
    assert "document" in response_dict, "Response should contain 'document' key"

    document = cast(dict, response_dict["document"])

    for field in _DOCUMENT_FIELDS:
        assert field in document, f"Field '{field}' should be present"

    assert int(document.get("id", 0)) == document_id, "Document ID does not match"
    assert document.get("entityTypeId") == str(_ENTITY_TYPE_ID), "Entity type ID does not match"
    assert document.get("entityId") == str(_ENTITY_ID), "Entity ID does not match"
    assert document.get("templateId") == str(_TEMPLATE_ID), "Template ID does not match"
    assert document.get("stampsEnabled") == _STAMPS_ENABLED, "Stamps enabled does not match"


@pytest.mark.dependency(name="test_crm_documentgenerator_document_list", depends=["test_crm_documentgenerator_document_get"])
def test_crm_documentgenerator_document_list(bitrix_client: Client, cache: Cache):
    """"""

    document_id = cache.get("created_document_id", None)
    assert isinstance(document_id, int), "Document ID should be cached"

    bitrix_response = bitrix_client.crm.documentgenerator.document.list(
        filter=_FILTER,
        start=_START,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    response_dict = cast(dict, bitrix_response.result)
    assert "documents" in response_dict, "Response should contain 'documents' key"

    documents = cast(list, response_dict["documents"])

    assert len(documents) >= 1, "Expected at least one document to be returned"

    for document in documents:
        assert isinstance(document, dict)
        if all((
                document.get("id") == str(document_id),
                document.get("entityTypeId") == str(_ENTITY_TYPE_ID),
                document.get("entityId") == str(_ENTITY_ID),
        )):
            break
    else:
        pytest.fail(f"Test document with ID {document_id} should be found in list")


@pytest.mark.dependency(name="test_crm_documentgenerator_document_list_as_list", depends=["test_crm_documentgenerator_document_list"])
def test_crm_documentgenerator_document_list_as_list(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.crm.documentgenerator.document.list().as_list().response

    assert isinstance(bitrix_response, BitrixAPIListResponse)
    assert isinstance(bitrix_response.result, list)

    documents = cast(list, bitrix_response.result)

    for document in documents:
        assert isinstance(document, dict)


@pytest.mark.dependency(name="test_crm_documentgenerator_document_update", depends=["test_crm_documentgenerator_document_list_as_list"])
def test_crm_documentgenerator_document_update(bitrix_client: Client, cache: Cache):
    """"""

    document_id = cache.get("created_document_id", None)
    assert isinstance(document_id, int), "Created document ID should be cached"

    bitrix_response = bitrix_client.crm.documentgenerator.document.update(
        bitrix_id=document_id,
        values=_VALUES,
        stamps_enabled=False,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    response_dict = cast(dict, bitrix_response.result)
    assert "document" in response_dict, "Response should contain 'document' key"

    updated_document = cast(dict, response_dict["document"])

    assert updated_document.get("id") == str(document_id), "Document ID should remain the same"
    assert updated_document.get("stampsEnabled") is False, "Document stamps enabled should be updated"


@pytest.mark.dependency(name="test_crm_documentgenerator_document_enablepublicurl", depends=["test_crm_documentgenerator_document_update"])
def test_crm_documentgenerator_document_enablepublicurl(bitrix_client: Client, cache: Cache):
    """"""

    document_id = cache.get("created_document_id", None)
    assert isinstance(document_id, int), "Created document ID should be cached"

    bitrix_response = bitrix_client.crm.documentgenerator.document.enablepublicurl(
        bitrix_id=document_id,
        status=True,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    result = cast(dict, bitrix_response.result)
    assert "publicUrl" in result, "Response should contain 'publicUrl'"


# @pytest.mark.dependency(name="test_crm_documentgenerator_document_upload", depends=["test_crm_documentgenerator_document_enablepublicurl"])
# def test_crm_documentgenerator_document_upload(bitrix_client: Client):
#     """"""
#
#     unique_title = f"{_TITLE}_{int(Config().get_local_datetime().timestamp() * (10 ** 6))}"
#     unique_number = int(Config().get_local_datetime().timestamp() * (10 ** 6)) % 10000
#
#     bitrix_response = bitrix_client.crm.documentgenerator.document.upload(
#         file_content=_FILE_CONTENT,
#         region=_REGION,
#         entity_type_id=_ENTITY_TYPE_ID,
#         entity_id=_ENTITY_ID,
#         title=unique_title,
#         number=unique_number,
#     ).response
#
#     assert isinstance(bitrix_response, BitrixAPIResponse)
#     assert isinstance(bitrix_response.result, dict)
#
#     response_dict = cast(dict, bitrix_response.result)
#     assert "document" in response_dict, "Response should contain 'document' key"
#
#     uploaded_document = cast(dict, response_dict["document"])
#
#     assert uploaded_document.get("title") == unique_title, "Document title should match"
#     assert int(uploaded_document.get("number", 0)) == unique_number, "Document number should match"


@pytest.mark.dependency(name="test_crm_documentgenerator_document_delete", depends=["test_crm_documentgenerator_document_enablepublicurl"])
def test_crm_documentgenerator_document_delete(bitrix_client: Client, cache: Cache):
    """"""

    document_id = cache.get("created_document_id", None)
    assert isinstance(document_id, int), "Created document ID should be cached"

    bitrix_response = bitrix_client.crm.documentgenerator.document.delete(
        bitrix_id=document_id,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
