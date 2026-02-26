from functools import cached_property
from typing import Iterable, Optional, Text

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity
from .chat import Chat
from .counters import Counters
from .favorite import Favorite
from .file import File
from .history import History
from .result import Result

__all__ = [
    "Task",
]


class Task(BaseEntity):
    """"""

    @cached_property
    def chat(self) -> Chat:
        """"""
        return Chat(self)

    @cached_property
    def counters(self) -> Counters:
        """"""
        return Counters(self)

    @cached_property
    def favorite(self) -> Favorite:
        """"""
        return Favorite(self)

    @cached_property
    def file(self) -> File:
        """"""
        return File(self)

    @cached_property
    def history(self) -> History:
        """"""
        return History(self)

    @cached_property
    def result(self) -> Result:
        """"""
        return Result(self)

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def approve(
            self,
            task_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "taskId": task_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.approve,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def complete(
            self,
            task_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "taskId": task_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.complete,
            params=params,
            timeout=timeout,
        )

    def delete(
            self,
            task_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "taskId": task_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delegate(
            self,
            task_id: int,
            user_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "taskId": task_id,
            "userId": user_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delegate,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def disapprove(
            self,
            task_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "taskId": task_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.disapprove,
            params=params,
            timeout=timeout,
        )

    def get(
            self,
            bitrix_id: int,
            *,
            select: Optional[Iterable[Text]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "id": bitrix_id,
        }

        if select is not None:
            if select.__class__ is not list:
                select = list(select)

            params["select"] = select

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get_fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._make_bitrix_api_request(
            api_wrapper=self.get_fields,
            timeout=timeout,
        )

    @type_checker
    def getaccess(
            self,
            task_id: int,
            *,
            users: Optional[Iterable[int]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "taskId": task_id,
        }

        if users is not None:
            if users.__class__ is not list:
                users = list(users)

            params["users"] = users

        return self._make_bitrix_api_request(
            api_wrapper=self.getaccess,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            *,
            order: Optional[JSONDict] = None,
            filter: Optional[JSONDict] = None,
            select: Optional[Iterable[Text]] = None,
            params: Optional[JSONDict] = None,
            start: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        _params = dict()

        if order is not None:
            _params["order"] = order

        if filter is not None:
            _params["filter"] = filter

        if select is not None:
            if select.__class__ is not list:
                select = list(select)

            _params["select"] = select

        if params is not None:
            _params["params"] = params

        if start is not None:
            _params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=_params,
            timeout=timeout,
        )

    @type_checker
    def renew(
            self,
            task_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "taskId": task_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.renew,
            params=params,
            timeout=timeout,
        )

    def start(
            self,
            task_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "taskId": task_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.start,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def startwatch(
            self,
            task_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "taskId": task_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.startwatch,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def unmute(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.unmute,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            task_id: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "taskId": task_id,
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
