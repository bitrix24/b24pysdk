import pytest

from b24pysdk.api.responses import BitrixAPIValueResponse, BitrixAPIValuesResponse
from b24pysdk.client import BaseClient
from b24pysdk.constants.userfield import UserTypeID
from b24pysdk.schemas.crm.userfield import CRMUserfieldField, CRMUserfieldFieldsDict, CRMUserfieldType

pytestmark = [
    pytest.mark.integration,
    pytest.mark.scopes,
    pytest.mark.crm,
    pytest.mark.crm_userfield,
]


def _assert_userfield_fields(bitrix_response: BitrixAPIValueResponse):
    assert isinstance(bitrix_response, BitrixAPIValueResponse)
    assert isinstance(bitrix_response.value, CRMUserfieldFieldsDict)

    userfield_fields = bitrix_response.value

    assert userfield_fields, "Expected at least one user field metadata field to be returned"

    for field_name, userfield_field in userfield_fields.items():
        assert isinstance(field_name, str)
        assert field_name
        assert isinstance(userfield_field, CRMUserfieldField)
        assert isinstance(userfield_field.type, str)
        assert userfield_field.type
        assert isinstance(userfield_field.title, str)
        assert userfield_field.title

        if userfield_field.is_read_only is not None:
            assert isinstance(userfield_field.is_read_only, bool)

        if userfield_field.is_immutable is not None:
            assert isinstance(userfield_field.is_immutable, bool)

        if userfield_field.is_multiple is not None:
            assert isinstance(userfield_field.is_multiple, bool)


def test_crm_userfield_types(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.crm.userfield.types().response

    assert isinstance(bitrix_response, BitrixAPIValuesResponse)
    assert isinstance(bitrix_response.result, list)

    userfield_types = bitrix_response.values

    assert userfield_types, "Expected at least one user field type to be returned"

    for userfield_type in userfield_types:
        assert isinstance(userfield_type, CRMUserfieldType)
        assert isinstance(userfield_type.bitrix_id, UserTypeID)
        assert isinstance(userfield_type.bitrix_id.value, str)
        assert userfield_type.bitrix_id.value
        assert isinstance(userfield_type.title, str)
        assert userfield_type.title


def test_crm_userfield_fields(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.crm.userfield.fields().response

    _assert_userfield_fields(bitrix_response)

    assert "ID" in bitrix_response.value
    assert "FIELD_NAME" in bitrix_response.value

    field_name_field = bitrix_response.value["FIELD_NAME"]
    assert field_name_field.is_immutable is True


def test_crm_userfield_enumeration_fields(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.crm.userfield.enumeration.fields().response

    _assert_userfield_fields(bitrix_response)

    assert "ID" in bitrix_response.value
    assert "VALUE" in bitrix_response.value


def test_crm_userfield_settings_fields(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.crm.userfield.settings.fields(
        type=UserTypeID.DOUBLE.value,
    ).response

    _assert_userfield_fields(bitrix_response)

    assert "DEFAULT_VALUE" in bitrix_response.value
    assert "PRECISION" in bitrix_response.value
