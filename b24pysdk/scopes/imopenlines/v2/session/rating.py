from typing import Iterable, Literal, Text

from ....._constants import MISSING
from .....api.requests import BitrixAPIRequest
from .....utils.converters import bool_to_bitrix
from .....utils.functional import classproperty, type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity

__all__ = [
    "Rating",
]


class Rating(BaseEntity):
    """"""

    @classproperty
    def _name(cls) -> Text:
        return "Rating"

    @type_checker
    def list(  # noqa: C901, PLR0912
            self,
            date_vote_from: Text,
            date_vote_to: Text,
            *,
            config_id: int = MISSING,
            config_id_list: Iterable[int] = MISSING,
            operator_id: int = MISSING,
            operator_id_list: Iterable[int] = MISSING,
            source: Text = MISSING,
            source_list: Iterable[Text] = MISSING,
            vote: Literal["like", "dislike"] = MISSING,
            has_vote_head: bool = MISSING,
            offset: int = MISSING,
            limit: int = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONDict]:
        """"""

        params: JSONDict = {
            "dateVoteFrom": date_vote_from,
            "dateVoteTo": date_vote_to,
        }

        if config_id is not MISSING:
            params["configId"] = config_id

        if config_id_list is not MISSING:
            if config_id_list.__class__ is not list:
                config_id_list = list(config_id_list)

            params["configIdList"] = config_id_list

        if operator_id is not MISSING:
            params["operatorId"] = operator_id

        if operator_id_list is not MISSING:
            if operator_id_list.__class__ is not list:
                operator_id_list = list(operator_id_list)

            params["operatorIdList"] = operator_id_list

        if source is not MISSING:
            params["source"] = source

        if source_list is not MISSING:
            if source_list.__class__ is not list:
                source_list = list(source_list)

            params["sourceList"] = source_list

        if vote is not MISSING:
            params["vote"] = vote

        if has_vote_head is not MISSING:
            params["hasVoteHead"] = bool_to_bitrix(has_vote_head, is_required=True)

        if offset is not MISSING:
            params["offset"] = offset

        if limit is not MISSING:
            params["limit"] = limit

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )
