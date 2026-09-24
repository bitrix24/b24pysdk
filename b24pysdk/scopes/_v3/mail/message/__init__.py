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
    """Methods for working with e-mails in mail.

    Documentation: https://apidocs.bitrix24.com/api-reference/mail/message/index.html
    """

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
        """Create a calendar event from an e-mail

        Documentation: https://apidocs.bitrix24.com/api-reference/mail/message/mail-message-createcalendarevent.html

        The method creates a calendar event from an e-mail.

        Args:
            message_id: E-mail identifier;

            date_from: Event start date and time in Y-m-d H:i:s format;

            date_to: Event end date and time in Y-m-d H:i:s format;

            name: Event name;

            description: Event description;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

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
        """Create a chat from e-mail

        Documentation: https://apidocs.bitrix24.com/api-reference/mail/message/mail-message-createchat.html

        The method

        Args:
            message_id: E-mail identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

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
        """Create a CRM activity from an e-mail

        Documentation: https://apidocs.bitrix24.com/api-reference/mail/message/mail-message-createcrmactivity.html

        The method creates a CRM activity from an e-mail.

        Args:
            message_id: E-mail identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

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
        """Create a news feed message from e-mail

        Documentation: https://apidocs.bitrix24.com/api-reference/mail/message/mail-message-createfeedpost.html

        The method creates a news feed message from an e-mail.

        Args:
            message_id: E-mail identifier;

            title: Message subject;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

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
        """Create a task from an e-mail

        Documentation: https://apidocs.bitrix24.com/api-reference/mail/message/mail-message-createtask.html

        The method creates a task from an e-mail.

        Args:
            message_id: E-mail identifier;

            title: Task name;

            responsible_id: Responsible person identifier;

            description: Task description;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

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
        """Forward e-mail

        Documentation: https://apidocs.bitrix24.com/api-reference/mail/message/mail-message-forward.html

        The method forwards an e-mail.

        Args:
            forward_message_id: E-mail identifier to be forwarded;

            from_: Message sender identifier;

            to: An array of recipient e-mail addresses;

            subject: E-mail subject;

            body: E-mail text: plain text or basic HTML;

            cc: An array of CC recipient e-mail addresses;

            bcc: An array of BCC recipient e-mail addresses;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

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
        """Geet e-mail

        Documentation: https://apidocs.bitrix24.com/api-reference/mail/message/mail-message-get.html

        The method retrieves an e-mail by its identifier.

        Args:
            bitrix_id: E-mail identifier;

            select: List of e-mail fields to be returned;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

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
        """Get a list of e-mails

        Documentation: https://apidocs.bitrix24.com/api-reference/mail/message/mail-message-list.html

        The method returns a list of e-mails based on specified conditions.

        Args:
            mailbox_id: Mailbox identifier;

            search_query: A string for searching e-mails by content and e-mail metadata;

            date_from: Date from which e-mails should be fetched;

            date_to: Date to which e-mails should be fetched;

            is_seen: Filter by e-mail read status;

            has_attachments: Filter by attachment presence;

            folder: Mail folder name or path;

            pagination: Pagination parameters;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

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
        """Move e-mails to folder

        Documentation: https://apidocs.bitrix24.com/api-reference/mail/message/mail-message-movetofolder.html

        The method moves e-mails to a folder, spam, or the trash.

        Args:
            message_ids: An array of e-mail IDs;

            action: Action for e-mails;

            folder: The name or path of an existing folder in the mailbox;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

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
        """Remove CRM activity

        Documentation: https://apidocs.bitrix24.com/api-reference/mail/message/mail-message-removecrmactivity.html

        The method removes the link between an e-mail and a CRM deal.

        Args:
            message_id: E-mail identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

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
        """Reply to e-mail

        Documentation: https://apidocs.bitrix24.com/api-reference/mail/message/mail-message-reply.html

        The method sends a reply to an e-mail.

        Args:
            reply_to_message_id: The e-mail identifier that needs to be replied to;

            from_: Sender's e-mail;

            to: An array of recipient e-mail addresses;

            subject: The e-mail subject;

            body: The e-mail body;

            cc: An array of CC recipient e-mail addresses;

            bcc: An array of BCC recipient e-mail addresses;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

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
        """Send an e-mail

        Documentation: https://apidocs.bitrix24.com/api-reference/mail/message/mail-message-send.html

        The method sends a new e-mail on behalf of an available sender.

        Args:
            from_: Sender's e-mail;

            to: An array of recipient e-mail addresses;

            subject: The e-mail subject;

            body: E-mail body;

            cc: An array of CC recipient e-mail addresses;

            bcc: An array of BCC recipient e-mail addresses;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

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
        """Get e-mail thread

        Documentation: https://apidocs.bitrix24.com/api-reference/mail/message/mail-message-thread.html

        The method returns an e-mail thread by their identifier of a single e-mail.

        Args:
            bitrix_id: The identifier of any e-mail from the thread;

            limit: The maximum number of e-mails to return;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

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
