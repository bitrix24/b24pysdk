from typing import Annotated, Iterable, Literal, Optional, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import classproperty, type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "AttachedVote",
]


class AttachedVote(BaseEntity):
    """Class for managing votes.

    Documentation: https://apidocs.bitrix24.com/api-reference/vote/index.html
    """

    @classproperty
    def _name(cls):
        return "AttachedVote"

    @type_checker
    def download(
            self,
            *,
            attach_id: Optional[int] = MISSING,
            module_id: Optional[Annotated[Text, Literal["Im", "blog"]]] = MISSING,
            entity_type: Optional[Annotated[
                Text,
                Literal["Bitrix\\Vote\\Attachment\\ImMessageConnector", "Bitrix\\Vote\\Attachment\\BlogPostConnector"],
            ]] = MISSING,
            entity_id: Optional[int] = MISSING,
            signed_attach_id: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Download the voting report

        Documentation: https://apidocs.bitrix24.com/api-reference/vote/vote.attachedvote.download.html

        The method generates and provides a downloadable report for the vote in the specified format.

        Args:
            attach_id: The ID of the attached vote;

            module_id: The module ID;

            entity_type: The object type;

            entity_id: The ID of the entity;

            signed_attach_id: The signed ID of the attachment;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if attach_id is not MISSING:
            params["attachId"] = attach_id

        if module_id is not MISSING:
            params["moduleId"] = module_id

        if entity_type is not MISSING:
            params["entityType"] = entity_type

        if entity_id is not MISSING:
            params["entityId"] = entity_id

        if signed_attach_id is not MISSING:
            params["signedAttachId"] = signed_attach_id

        return self._make_bitrix_api_request(
            api_wrapper=self.download,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            *,
            attach_id: Optional[int] = MISSING,
            module_id: Optional[Annotated[Text, Literal["Im", "blog"]]] = MISSING,
            entity_type: Optional[Annotated[
                Text,
                Literal["Bitrix\\Vote\\Attachment\\ImMessageConnector", "Bitrix\\Vote\\Attachment\\BlogPostConnector"],
            ]] = MISSING,
            entity_id: Optional[int] = MISSING,
            signed_attach_id: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get data of attached vote

        Documentation: https://apidocs.bitrix24.com/api-reference/vote/vote.attachedvote.get.html

        The method returns data of the attached vote.

        Args:
            attach_id: The ID of the attached vote;

            module_id: The module ID;

            entity_type: The object type;

            entity_id: The ID of the entity;

            signed_attach_id: The signed ID of the attachment;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if attach_id is not MISSING:
            params["attachId"] = attach_id

        if module_id is not MISSING:
            params["moduleId"] = module_id

        if entity_type is not MISSING:
            params["entityType"] = entity_type

        if entity_id is not MISSING:
            params["entityId"] = entity_id

        if signed_attach_id is not MISSING:
            params["signedAttachId"] = signed_attach_id

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get_answer_voted(
            self,
            answer_id: int,
            *,
            attach_id: Optional[int] = MISSING,
            page_navigation: Optional[JSONDict] = MISSING,
            user_for_mobile_format: Optional[bool] = MISSING,
            module_id: Optional[Annotated[Text, Literal["Im", "blog"]]] = MISSING,
            entity_type: Optional[Annotated[
                Text,
                Literal["Bitrix\\Vote\\Attachment\\ImMessageConnector", "Bitrix\\Vote\\Attachment\\BlogPostConnector"],
            ]] = MISSING,
            entity_id: Optional[int] = MISSING,
            signed_attach_id: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the list of users who voted for the answer

        Documentation: https://apidocs.bitrix24.com/api-reference/vote/vote.attachedvote.getAnswerVoted.html

        The method returns a list of users who voted for the specified answer option.

        Args:
            attach_id: The ID of the attached vote;

            page_navigation: Pagination parameters;

            user_for_mobile_format: User data format for mobile devices;

            module_id: The module ID;

            entity_type: The object type;

            entity_id: The ID of the entity;

            signed_attach_id: The signed ID of the attachment;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "answerId": answer_id,
        }

        if attach_id is not MISSING:
            params["attachId"] = attach_id

        if page_navigation is not MISSING:
            params["pageNavigation"] = page_navigation

        if user_for_mobile_format is not MISSING:
            params["userForMobileFormat"] = user_for_mobile_format

        if module_id is not MISSING:
            params["moduleId"] = module_id

        if entity_type is not MISSING:
            params["entityType"] = entity_type

        if entity_id is not MISSING:
            params["entityId"] = entity_id

        if signed_attach_id is not MISSING:
            params["signedAttachId"] = signed_attach_id

        return self._make_bitrix_api_request(
            api_wrapper=self.get_answer_voted,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get_many(
            self,
            module_id: Annotated[Text, Literal["Im", "blog"]],
            entity_type: Annotated[
                Text,
                Literal["Bitrix\\Vote\\Attachment\\ImMessageConnector", "Bitrix\\Vote\\Attachment\\BlogPostConnector"],
            ],
            entity_ids: Iterable[int],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get multiple votes

        Documentation: https://apidocs.bitrix24.com/api-reference/vote/vote.attachedvote.getMany.html

        The method returns data for multiple votes based on the identifier of the entities to which vote is attached.

        Args:
            module_id: The module ID;

            entity_type: The object type;

            entity_ids: Array of entity identifiers;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        if entity_ids.__class__ is not list:
            entity_ids = list(entity_ids)

        params = {
            "moduleId": module_id,
            "entityType": entity_type,
            "entityIds": entity_ids,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get_many,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get_with_voted(
            self,
            *,
            attach_id: Optional[int] = MISSING,
            page_size: Optional[int] = MISSING,
            user_for_mobile_format: Optional[bool] = MISSING,
            module_id: Optional[Annotated[Text, Literal["Im", "blog"]]] = MISSING,
            entity_type: Optional[Annotated[
                Text,
                Literal["Bitrix\\Vote\\Attachment\\ImMessageConnector", "Bitrix\\Vote\\Attachment\\BlogPostConnector"],
            ]] = MISSING,
            entity_id: Optional[int] = MISSING,
            signed_attach_id: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get voting data with voter information

        Documentation: https://apidocs.bitrix24.com/api-reference/vote/vote.attachedvote.getWithVoted.html

        The method returns data for attached vote along with information about the users who voted.

        Args:
            attach_id: The ID of the attached vote;

            page_size: Pagination parameters;

            user_for_mobile_format: User data format for mobile devices;

            module_id: The module ID;

            entity_type: The object type;

            entity_id: The ID of the entity;

            signed_attach_id: The signed ID of the attachment;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if attach_id is not MISSING:
            params["attachId"] = attach_id

        if page_size is not MISSING:
            params["pageSize"] = page_size

        if user_for_mobile_format is not MISSING:
            params["userForMobileFormat"] = user_for_mobile_format

        if module_id is not MISSING:
            params["moduleId"] = module_id

        if entity_type is not MISSING:
            params["entityType"] = entity_type

        if entity_id is not MISSING:
            params["entityId"] = entity_id

        if signed_attach_id is not MISSING:
            params["signedAttachId"] = signed_attach_id

        return self._make_bitrix_api_request(
            api_wrapper=self.get_with_voted,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def recall(
            self,
            *,
            attach_id: Optional[int] = MISSING,
            module_id: Optional[Annotated[Text, Literal["Im", "blog"]]] = MISSING,
            entity_type: Optional[Annotated[
                Text,
                Literal["Bitrix\\Vote\\Attachment\\ImMessageConnector", "Bitrix\\Vote\\Attachment\\BlogPostConnector"],
            ]] = MISSING,
            entity_id: Optional[int] = MISSING,
            signed_attach_id: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Recall your vote

        Documentation: https://apidocs.bitrix24.com/api-reference/vote/vote.attachedvote.recall.html

        The method allows a user to withdraw their vote in an active voting session.

        Args:
            attach_id: The ID of the attached vote;

            module_id: The module ID;

            entity_type: The object type;

            entity_id: The ID of the entity;

            signed_attach_id: The signed ID of the attachment;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if attach_id is not MISSING:
            params["attachId"] = attach_id

        if module_id is not MISSING:
            params["moduleId"] = module_id

        if entity_type is not MISSING:
            params["entityType"] = entity_type

        if entity_id is not MISSING:
            params["entityId"] = entity_id

        if signed_attach_id is not MISSING:
            params["signedAttachId"] = signed_attach_id

        return self._make_bitrix_api_request(
            api_wrapper=self.recall,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def resume(
            self,
            *,
            attach_id: Optional[int] = MISSING,
            module_id: Optional[Annotated[Text, Literal["Im", "blog"]]] = MISSING,
            entity_type: Optional[Annotated[
                Text,
                Literal["Bitrix\\Vote\\Attachment\\ImMessageConnector", "Bitrix\\Vote\\Attachment\\BlogPostConnector"],
            ]] = MISSING,
            entity_id: Optional[int] = MISSING,
            signed_attach_id: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Resume voting

        Documentation: https://apidocs.bitrix24.com/api-reference/vote/vote.attachedvote.resume.html

        The method resumes a stopped vote, allowing users to participate in it again.

        Args:
            attach_id: The ID of the attached vote;

            module_id: The module ID;

            entity_type: The object type;

            entity_id: The ID of the entity;

            signed_attach_id: The signed ID of the attachment;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if attach_id is not MISSING:
            params["attachId"] = attach_id

        if module_id is not MISSING:
            params["moduleId"] = module_id

        if entity_type is not MISSING:
            params["entityType"] = entity_type

        if entity_id is not MISSING:
            params["entityId"] = entity_id

        if signed_attach_id is not MISSING:
            params["signedAttachId"] = signed_attach_id

        return self._make_bitrix_api_request(
            api_wrapper=self.resume,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def stop(
            self,
            *,
            attach_id: Optional[int] = MISSING,
            module_id: Optional[Annotated[Text, Literal["Im", "blog"]]] = MISSING,
            entity_type: Optional[Annotated[
                Text,
                Literal["Bitrix\\Vote\\Attachment\\ImMessageConnector", "Bitrix\\Vote\\Attachment\\BlogPostConnector"],
            ]] = MISSING,
            entity_id: Optional[int] = MISSING,
            signed_attach_id: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Stop voting

        Documentation: https://apidocs.bitrix24.com/api-reference/vote/vote.attachedvote.stop.html

        The method halts an active vote, preventing further participation.

        Args:
            attach_id: The ID of the attached vote;

            module_id: The module ID;

            entity_type: The object type;

            entity_id: The ID of the entity;

            signed_attach_id: The signed ID of the attachment;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if attach_id is not MISSING:
            params["attachId"] = attach_id

        if module_id is not MISSING:
            params["moduleId"] = module_id

        if entity_type is not MISSING:
            params["entityType"] = entity_type

        if entity_id is not MISSING:
            params["entityId"] = entity_id

        if signed_attach_id is not MISSING:
            params["signedAttachId"] = signed_attach_id

        return self._make_bitrix_api_request(
            api_wrapper=self.stop,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def vote(
            self,
            ballot: JSONDict,
            *,
            attach_id: Optional[int] = MISSING,
            module_id: Optional[Annotated[Text, Literal["Im", "blog"]]] = MISSING,
            entity_type: Optional[Annotated[
                Text,
                Literal["Bitrix\\Vote\\Attachment\\ImMessageConnector", "Bitrix\\Vote\\Attachment\\BlogPostConnector"],
            ]] = MISSING,
            entity_id: Optional[int] = MISSING,
            signed_attach_id: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Vote in the attached voting

        Documentation: https://apidocs.bitrix24.com/api-reference/vote/vote.attachedvote.vote.html

        The method allows you to vote in an attached voting.

        Args:
            ballot: Voting data;

            attach_id: The ID of the attached vote;

            module_id: The module ID;

            entity_type: The object type;

            entity_id: The ID of the entity;

            signed_attach_id: The signed ID of the attachment;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "ballot": ballot,
        }

        if attach_id is not MISSING:
            params["attachId"] = attach_id

        if module_id is not MISSING:
            params["moduleId"] = module_id

        if entity_type is not MISSING:
            params["entityType"] = entity_type

        if entity_id is not MISSING:
            params["entityId"] = entity_id

        if signed_attach_id is not MISSING:
            params["signedAttachId"] = signed_attach_id

        return self._make_bitrix_api_request(
            api_wrapper=self.vote,
            params=params,
            timeout=timeout,
        )
