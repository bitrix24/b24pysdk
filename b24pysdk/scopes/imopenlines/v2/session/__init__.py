from functools import cached_property
from typing import Iterable, Literal, Text

from ....._constants import MISSING
from .....api.requests import BitrixAPIRequest
from .....utils.converters import bool_to_bitrix
from .....utils.functional import classproperty, type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity
from .rating import Rating
from .stat import Stat
from .transfer import Transfer

__all__ = [
    "Session",
]


class Session(BaseEntity):
    """"""

    @classproperty
    def _name(cls) -> Text:
        return "Session"

    @cached_property
    def rating(self) -> Rating:
        """"""
        return Rating(self)

    @cached_property
    def stat(self) -> Stat:
        """"""
        return Stat(self)

    @cached_property
    def transfer(self) -> Transfer:
        """"""
        return Transfer(self)

    @type_checker
    def list(  # noqa: C901, PLR0912, PLR0915
            self,
            *,
            config_id: int = MISSING,
            config_id_list: Iterable[int] = MISSING,
            operator_id: int = MISSING,
            operator_id_list: Iterable[int] = MISSING,
            source: Text = MISSING,
            source_list: Iterable[Text] = MISSING,
            status: Literal["new", "answered", "closed", "spam", "paused"] = MISSING,
            close_reason: Literal["operator", "auto", "spam", "client", "replyLimit"] = MISSING,
            date_create_from: Text = MISSING,
            date_create_to: Text = MISSING,
            date_close_from: Text = MISSING,
            date_close_to: Text = MISSING,
            vote: Literal["like", "dislike", "none", "any"] = MISSING,
            has_vote_head: bool = MISSING,
            kpi_first_answer: bool = MISSING,
            has_crm: bool = MISSING,
            wait_answer_from: int = MISSING,
            wait_answer_to: int = MISSING,
            wait_close_from: int = MISSING,
            wait_close_to: int = MISSING,
            order: Literal["dateCreate", "dateClose", "waitAnswer", "waitClose"] = MISSING,
            order_direction: Literal["asc", "desc"] = MISSING,
            offset: int = MISSING,
            limit: int = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {}

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

        if status is not MISSING:
            params["status"] = status

        if close_reason is not MISSING:
            params["closeReason"] = close_reason

        if date_create_from is not MISSING:
            params["dateCreateFrom"] = date_create_from

        if date_create_to is not MISSING:
            params["dateCreateTo"] = date_create_to

        if date_close_from is not MISSING:
            params["dateCloseFrom"] = date_close_from

        if date_close_to is not MISSING:
            params["dateCloseTo"] = date_close_to

        if vote is not MISSING:
            params["vote"] = vote

        if has_vote_head is not MISSING:
            params["hasVoteHead"] = bool_to_bitrix(has_vote_head, is_required=True)

        if kpi_first_answer is not MISSING:
            params["kpiFirstAnswer"] = bool_to_bitrix(kpi_first_answer, is_required=True)

        if has_crm is not MISSING:
            params["hasCrm"] = bool_to_bitrix(has_crm, is_required=True)

        if wait_answer_from is not MISSING:
            params["waitAnswerFrom"] = wait_answer_from

        if wait_answer_to is not MISSING:
            params["waitAnswerTo"] = wait_answer_to

        if wait_close_from is not MISSING:
            params["waitCloseFrom"] = wait_close_from

        if wait_close_to is not MISSING:
            params["waitCloseTo"] = wait_close_to

        if order is not MISSING:
            params["order"] = order

        if order_direction is not MISSING:
            params["orderDirection"] = order_direction

        if offset is not MISSING:
            params["offset"] = offset

        if limit is not MISSING:
            params["limit"] = limit

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params or None,
            timeout=timeout,
        )
