from functools import cached_property
from typing import Iterable, Optional, Text

from ....._constants import MISSING
from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity
from .field import Field

__all__ = [
    "Message",
]


class Message(BaseEntity):
    """"""

    @cached_property
    def field(self) -> Field:
        """"""
        return Field(self)

    @type_checker
    def createcalendarevent(
            self,
            message_id: int,
            date_from: Text,
            date_to: Text,
            *,
            name: Optional[Text] = MISSING,
            description: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "messageId": message_id,
            "dateFrom": date_from,
            "dateTo": date_to,
        }

        if name is not MISSING:
            params["name"] = name

        if description is not MISSING:
            params["description"] = description

        return self._make_bitrix_api_request(
            api_wrapper=self.createcalendarevent,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def createchat(
            self,
            message_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "messageId": message_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.createchat,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def createcrmactivity(
            self,
            message_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "messageId": message_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.createcrmactivity,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def createfeedpost(
            self,
            message_id: int,
            *,
            title: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "messageId": message_id,
        }

        if title is not MISSING:
            params["title"] = title

        return self._make_bitrix_api_request(
            api_wrapper=self.createfeedpost,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def createtask(
            self,
            message_id: int,
            *,
            title: Optional[Text] = MISSING,
            responsible_id: Optional[int] = MISSING,
            description: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "messageId": message_id,
        }

        if title is not MISSING:
            params["title"] = title

        if responsible_id is not MISSING:
            params["responsibleId"] = responsible_id

        if description is not MISSING:
            params["description"] = description

        return self._make_bitrix_api_request(
            api_wrapper=self.createtask,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def forward(
            self,
            forward_message_id: int,
            from_: Text,
            to: Iterable[Text],
            subject: Text,
            body: Text,
            *,
            cc: Optional[Iterable[Text]] = MISSING,
            bcc: Optional[Iterable[Text]] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if to.__class__ is not list:
            to = list(to)

        params = {
            "forwardMessageId": forward_message_id,
            "from": from_,
            "to": to,
            "subject": subject,
            "body": body,
        }

        if cc is not MISSING:
            if cc.__class__ is not list:
                cc = list(cc)

            params["cc"] = cc

        if bcc is not MISSING:
            if bcc.__class__ is not list:
                bcc = list(bcc)

            params["bcc"] = bcc

        return self._make_bitrix_api_request(
            api_wrapper=self.forward,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            bitrix_id: int,
            *,
            select: Optional[Iterable[Text]] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "id": bitrix_id,
        }

        if select is not MISSING:
            if select.__class__ is not list:
                select = list(select)

            params["select"] = select

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            mailbox_id: int,
            *,
            search_query: Optional[Text] = MISSING,
            date_from: Optional[Text] = MISSING,
            date_to: Optional[Text] = MISSING,
            is_seen: Optional[bool] = MISSING,
            has_attachments: Optional[bool] = MISSING,
            folder: Optional[Text] = MISSING,
            pagination: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "mailboxId": mailbox_id,
        }

        if search_query is not MISSING:
            params["searchQuery"] = search_query

        if date_from is not MISSING:
            params["dateFrom"] = date_from

        if date_to is not MISSING:
            params["dateTo"] = date_to

        if is_seen is not MISSING:
            params["isSeen"] = is_seen

        if has_attachments is not MISSING:
            params["hasAttachments"] = has_attachments

        if folder is not MISSING:
            params["folder"] = folder

        if pagination is not MISSING:
            params["pagination"] = pagination

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def movetofolder(
            self,
            message_ids: Iterable[int],
            action: Text,
            *,
            folder: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if message_ids.__class__ is not list:
            message_ids = list(message_ids)

        params = {
            "messageIds": message_ids,
            "action": action,
        }

        if folder is not MISSING:
            params["folder"] = folder

        return self._make_bitrix_api_request(
            api_wrapper=self.movetofolder,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def removecrmactivity(
            self,
            message_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "messageId": message_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.removecrmactivity,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def reply(
            self,
            reply_to_message_id: int,
            from_: Text,
            to: Iterable[Text],
            subject: Text,
            body: Text,
            *,
            cc: Optional[Iterable[Text]] = MISSING,
            bcc: Optional[Iterable[Text]] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if to.__class__ is not list:
            to = list(to)

        params = {
            "replyToMessageId": reply_to_message_id,
            "from": from_,
            "to": to,
            "subject": subject,
            "body": body,
        }

        if cc is not MISSING:
            if cc.__class__ is not list:
                cc = list(cc)

            params["cc"] = cc

        if bcc is not MISSING:
            if bcc.__class__ is not list:
                bcc = list(bcc)

            params["bcc"] = bcc

        return self._make_bitrix_api_request(
            api_wrapper=self.reply,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def send(
            self,
            from_: Text,
            to: Iterable[Text],
            subject: Text,
            body: Text,
            *,
            cc: Optional[Iterable[Text]] = MISSING,
            bcc: Optional[Iterable[Text]] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if to.__class__ is not list:
            to = list(to)

        params = {
            "from": from_,
            "to": to,
            "subject": subject,
            "body": body,
        }

        if cc is not MISSING:
            if cc.__class__ is not list:
                cc = list(cc)

            params["cc"] = cc

        if bcc is not MISSING:
            if bcc.__class__ is not list:
                bcc = list(bcc)

            params["bcc"] = bcc

        return self._make_bitrix_api_request(
            api_wrapper=self.send,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def thread(
            self,
            bitrix_id: int,
            *,
            limit: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "id": bitrix_id,
        }

        if limit is not MISSING:
            params["limit"] = limit

        return self._make_bitrix_api_request(
            api_wrapper=self.thread,
            params=params,
            timeout=timeout,
        )
