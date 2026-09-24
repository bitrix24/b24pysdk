import pytest

from b24pysdk.client import Client
from tests.unit.examples import TOKEN_MOCK

pytestmark = [
    pytest.mark.unit,
]


def test_get_supported_api_methods_smoke():
    methods = Client(TOKEN_MOCK).get_supported_api_methods()

    assert methods


def test_new_scope_methods_have_expected_api_paths():
    client = Client(TOKEN_MOCK)
    requests = [
        client.crm.activity.call.get_transcript(1),
        client.disk.file.search("report"),
        client.humanresources.hcmlink.company.add({}),
        client.humanresources.hcmlink.company.delete(1),
        client.humanresources.hcmlink.company.list(),
        client.humanresources.hcmlink.company.update(1, {}),
        client.humanresources.hcmlink.company.user.list(),
        client.humanresources.hcmlink.employee.list("company"),
        client.humanresources.hcmlink.employee.set("company", []),
        client.humanresources.hcmlink.field.value.set("company", []),
        client.humanresources.hcmlink.job.status.get(1),
        client.humanresources.hcmlink.job.update(1, {}),
        client.imopenlines.v2.session.rating.list("2026-01-01", "2026-01-31"),
    ]

    assert [request._api_method for request in requests] == [
        "crm.activity.call.getTranscript",
        "disk.file.search",
        "humanresources.hcmlink.company.add",
        "humanresources.hcmlink.company.delete",
        "humanresources.hcmlink.company.list",
        "humanresources.hcmlink.company.update",
        "humanresources.hcmlink.company.user.list",
        "humanresources.hcmlink.employee.list",
        "humanresources.hcmlink.employee.set",
        "humanresources.hcmlink.field.value.set",
        "humanresources.hcmlink.job.status.get",
        "humanresources.hcmlink.job.update",
        "imopenlines.v2.Session.Rating.list",
    ]


def test_new_scope_methods_build_expected_params():
    client = Client(TOKEN_MOCK)

    disk_search = client.disk.file.search(
        "report",
        type="all",
        filter={"STORAGE_ID": 1},
        start=0,
    )
    rating_list = client.imopenlines.v2.session.rating.list(
        "2026-01-01",
        "2026-01-31",
        config_id_list=(1, 2),
        has_vote_head=True,
    )

    assert disk_search._params == {
        "QUERY": "report",
        "TYPE": "all",
        "FILTER": {"STORAGE_ID": 1},
        "start": 0,
    }
    assert rating_list._params == {
        "dateVoteFrom": "2026-01-01",
        "dateVoteTo": "2026-01-31",
        "configIdList": [1, 2],
        "hasVoteHead": "Y",
    }
