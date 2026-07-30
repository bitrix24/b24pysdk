from typing import Iterable, Optional, Sequence, Text, Union

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.converters import bool_to_bitrix
from ...utils.functional import type_checker
from ...utils.types import B24File, JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Block",
]


class Block(BaseEntity):
    """Class for working with page fragments.

    Documentation: https://apidocs.bitrix24.com/api-reference/landing/block/index.html
    """

    @type_checker
    def addcard(
            self,
            lid: int,
            block: int,
            selector: Text,
            content: Text,
            *,
            scope: Optional[Text] = MISSING,
            prevent_history: Optional[bool] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add card to block

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/block/methods/landing-block-add-card.html

        The method adds a card to a block in the draft of a page.

        Args:
            lid: Identifier of the page;

            block: Identifier of the block in the editable version of the page;

            selector: Selector of the card from the key cards of the block manifest;

            content: HTML of the new card;

            scope: Internal scope of landings;

            prevent_history: Do not add the action to the page change history;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "lid": lid,
            "block": block,
            "selector": selector,
            "content": content,
        }

        if scope is not MISSING:
            params["scope"] = scope

        if prevent_history is not MISSING:
            params["preventHistory"] = bool_to_bitrix(prevent_history, is_required=True)

        return self._make_bitrix_api_request(
            api_wrapper=self.addcard,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def change_anchor(
            self,
            lid: int,
            block: int,
            data: Text,
            *,
            scope: Optional[Text] = MISSING,
            prevent_history: Optional[bool] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Change the anchor of the block

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/block/methods/landing-block-change-anchor.html

        The method modifies or removes a custom anchor of a block in the draft of a page.

        Args:
            lid: Identifier of the page;

            block: Identifier of the block in the editable version of the page;

            data: New anchor of the block without the # symbol;

            scope: Internal scope of landings;

            prevent_history: Do not add the action to the page change history;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest """

        params: JSONDict = {
            "lid": lid,
            "block": block,
            "data": data,
        }

        if scope is not MISSING:
            params["scope"] = scope

        if prevent_history is not MISSING:
            params["preventHistory"] = bool_to_bitrix(prevent_history, is_required=True)

        return self._make_bitrix_api_request(
            api_wrapper=self.change_anchor,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def change_node_name(
            self,
            lid: int,
            block: int,
            data: JSONDict,
            *,
            scope: Optional[Text] = MISSING,
            prevent_history: Optional[bool] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Change HTML tag of a block element

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/block/methods/landing-block-change-node-name.html

        The method changes the HTML tag of a block element in the draft of a page.

        Args:
            lid: Identifier of the page;

            block: Identifier of the block in the editable version of the page;

            data: New anchor of the block without the # symbol;

            scope: Internal scope of landings;

            prevent_history: Do not add the action to the page change history;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest """

        params: JSONDict = {
            "lid": lid,
            "block": block,
            "data": data,
        }

        if scope is not MISSING:
            params["scope"] = scope

        if prevent_history is not MISSING:
            params["preventHistory"] = bool_to_bitrix(prevent_history, is_required=True)

        return self._make_bitrix_api_request(
            api_wrapper=self.change_node_name,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def clonecard(
            self,
            lid: int,
            block: int,
            selector: Text,
            *,
            scope: Optional[Text] = MISSING,
            prevent_history: Optional[bool] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Clone card of block

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/block/methods/landing-block-clone-card.html

        The method creates a copy of a card in the block within the draft of the page.

        Args:
            lid: Identifier of the page;

            block: Identifier of the block in the editable version of the page;

            selector: Selector of the card from the key cards of the block manifest;

            scope: Internal scope of landings;

            prevent_history: Do not add the action to the page change history;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "lid": lid,
            "block": block,
            "selector": selector,
        }

        if scope is not MISSING:
            params["scope"] = scope

        if prevent_history is not MISSING:
            params["preventHistory"] = bool_to_bitrix(prevent_history, is_required=True)

        return self._make_bitrix_api_request(
            api_wrapper=self.clonecard,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get_content_from_repository(
            self,
            code: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get block content from repository

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/block/methods/landing-block-get-content-from-repository.html

        The method returns the HTML content of a block from the repository.

        Args:
            code: The code of the block whose content needs to be retrieved;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest"""

        api_params: JSONDict = {
            "code": code,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get_content_from_repository,
            params=api_params,
            timeout=timeout,
        )

    @type_checker
    def getbyid(
            self,
            block: int,
            *,
            scope: Optional[Text] = MISSING,
            params: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get block by ID

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/block/methods/landing-block-get-by-id.html

        The method returns a single block of a page by its identifier.

        Args:
            block: Identifier of the block in the editable version of the page;

            scope: Internal scope of landings;

            params: Additional parameters for reading the block;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        api_params: JSONDict = {
            "block": block,
        }

        if scope is not MISSING:
            api_params["scope"] = scope

        if params is not MISSING:
            api_params["params"] = params

        return self._make_bitrix_api_request(
            api_wrapper=self.getbyid,
            params=api_params,
            timeout=timeout,
        )

    @type_checker
    def getcontent(
            self,
            lid: int,
            block: int,
            *,
            scope: Optional[Text] = MISSING,
            edit_mode: Optional[int] = MISSING,
            params: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get content of block

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/block/methods/landing-block-get-content.html

        The method returns the ready HTML of the block, its resources, manifest, and service properties of the block.

        Args:
            lid: Identifier of the page;

            block: Identifier of the block in the editable version of the page;

            scope: Internal scope of landings;

            edit_mode: Mode for obtaining the version of the block;

            params: Additional parameters;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        api_params: JSONDict = {
            "lid": lid,
            "block": block,
        }

        if scope is not MISSING:
            api_params["scope"] = scope

        if edit_mode is not MISSING:
            api_params["editMode"] = edit_mode

        if params is not MISSING:
            api_params["params"] = params

        return self._make_bitrix_api_request(
            api_wrapper=self.getcontent,
            params=api_params or None,
            timeout=timeout,
        )

    @type_checker
    def getlist(
            self,
            lid: Union[int, Iterable[int]],
            *,
            scope: Optional[Text] = MISSING,
            params: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the List of page blocks

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/block/methods/landing-block-get-list.html

        The method returns a list of blocks for the selected page.

        Args:
            lid: Identifier of the page;

            scope: Internal scope of landings;

            params: Additional parameters;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        if lid.__class__ is not list and lid.__class__ is not int:
            lid = list(lid)

        api_params: JSONDict = {
            "lid": lid,
        }

        if scope is not MISSING:
            api_params["scope"] = scope

        if params is not MISSING:
            api_params["params"] = params

        return self._make_bitrix_api_request(
            api_wrapper=self.getlist,
            params=api_params or None,
            timeout=timeout,
        )

    @type_checker
    def getmanifest(
            self,
            lid: int,
            block: int,
            *,
            scope: Optional[Text] = MISSING,
            params: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the manifest of the landing

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/block/methods/landing-block-get-manifest.html

        The method returns a prepared manifest of the block placed on the page.

        Args:
            lid: Identifier of the page;

            block: Identifier of the block in the editable version of the page;

            scope: Internal scope of landings;

            params: Additional parameters;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        api_params: JSONDict = {
            "lid": lid,
            "block": block,
        }

        if scope is not MISSING:
            api_params["scope"] = scope

        if params is not MISSING:
            api_params["params"] = params

        return self._make_bitrix_api_request(
            api_wrapper=self.getmanifest,
            params=api_params or None,
            timeout=timeout,
        )

    @type_checker
    def getmanifestfile(
            self,
            code: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the manifest file of the landing

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/block/methods/landing-block-get-manifest-file.html

        The method returns the original manifest of the block from the file repository.

        Args:
            code: The code of the block from the file repository;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        api_params: JSONDict = {
            "code": code,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.getmanifestfile,
            params=api_params or None,
            timeout=timeout,
        )

    @type_checker
    def getrepository(
            self,
            *,
            section: Optional[Text] = MISSING,
            scope: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of blocks from the repository

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/block/methods/landing-block-get-repository.html

        The method returns the available sections of the block repository or the data for a specific section.

        Args:
            section: The code of the repository section;

            scope: Internal scope of landings;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        api_params: JSONDict = {}

        if section is not MISSING:
            api_params["section"] = section

        if scope is not MISSING:
            api_params["scope"] = scope

        return self._make_bitrix_api_request(
            api_wrapper=self.getrepository,
            params=api_params or None,
            timeout=timeout,
        )

    @type_checker
    def removecard(
            self,
            lid: int,
            block: int,
            selector: Text,
            *,
            scope: Optional[Text] = MISSING,
            prevent_history: Optional[bool] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Remove card from block

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/block/methods/landing-block-remove-card.html

        The method removes a card from a block in the draft of a page.

        Args:
            lid: Identifier of the page;

            block: Identifier of the block in the editable version of the page;

            selector: Selector of the card from the key cards of the block manifest;

            scope: Internal scope of landings;

            prevent_history: Do not add the action to the page change history;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "lid": lid,
            "block": block,
            "selector": selector,
        }

        if scope is not MISSING:
            params["scope"] = scope

        if prevent_history is not MISSING:
            params["preventHistory"] = bool_to_bitrix(prevent_history, is_required=True)

        return self._make_bitrix_api_request(
            api_wrapper=self.removecard,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update_cards(
            self,
            lid: int,
            block: int,
            data: JSONDict,
            *,
            scope: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update cards

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/block/methods/landing-block-update-cards.html

        The method updates a set of cards in a block and the nodes within those cards in the draft of the page.

        Args:
            lid: Identifier of the page;

            block: Identifier of the block in the editable version of the page;

            data: Set of changes for the block cards;

            scope: Internal scope of landings;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "lid": lid,
            "block": block,
            "data": data,
        }

        if scope is not MISSING:
            params["scope"] = scope

        return self._make_bitrix_api_request(
            api_wrapper=self.update_cards,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def updateattrs(
            self,
            lid: int,
            block: int,
            data: JSONDict,
            *,
            scope: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update attributes

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/block/methods/landing-block-update-attrs.html

        The method updates the attributes of HTML elements within a block in the draft of a page.

        Args:
            lid: Identifier of the page;

            block: Identifier of the block in the editable version of the page;

            data: Set of changes for the block cards;

            scope: Internal scope of landings;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "lid": lid,
            "block": block,
            "data": data,
        }

        if scope is not MISSING:
            params["scope"] = scope

        return self._make_bitrix_api_request(
            api_wrapper=self.updateattrs,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update_styles(
            self,
            lid: int,
            block: int,
            data: JSONDict,
            *,
            scope: Optional[Text] = MISSING,
            prevent_history: Optional[bool] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update styles

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/block/methods/landing-block-update-styles.html

        The method updates the CSS classes and inline styles of block elements in the draft of a page.

        Args:
            lid: Identifier of the page;

            block: Identifier of the block in the editable version of the page;

            data: Set of changes for the block cards;

            scope: Internal scope of landings;

            prevent_history: If true is passed, the method will not add the change to the page history;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "lid": lid,
            "block": block,
            "data": data,
        }

        if scope is not MISSING:
            params["scope"] = scope

        if prevent_history is not MISSING:
            params["preventHistory"] = bool_to_bitrix(prevent_history, is_required=True)

        return self._make_bitrix_api_request(
            api_wrapper=self.update_styles,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def updatecontent(
            self,
            lid: int,
            block: int,
            content: Text,
            *,
            scope: Optional[Text] = MISSING,
            designed: Optional[bool] = MISSING,
            prevent_history: Optional[bool] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update content of the block

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/block/methods/landing-block-update-content.html

        The method completely replaces the HTML content of a block in the page draft.

        Args:
            lid: Identifier of the page;

            block: Identifier of the block in the editable version of the page;

            scope: Internal scope of landings;

            designed: Marks the block as manually modified;

            prevent_history: If true is passed, the method will not add the change to the page history;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "lid": lid,
            "block": block,
            "content": content,
        }

        if scope is not MISSING:
            params["scope"] = scope

        if designed is not MISSING:
            params["designed"] = designed

        if prevent_history is not MISSING:
            params["preventHistory"] = bool_to_bitrix(prevent_history, is_required=True)

        return self._make_bitrix_api_request(
            api_wrapper=self.updatecontent,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def updatenodes(
            self,
            lid: int,
            block: int,
            data: JSONDict,
            *,
            scope: Optional[Text] = MISSING,
            additional: Optional[JSONDict] = MISSING,
            prevent_history: Optional[bool] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update nodes of the block

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/block/methods/landing-block-update-nodes.html

        The method updates the nodes of a block in the draft of a page.

        Args:
            lid: Identifier of the page;

            block: Identifier of the block in the editable version of the page;

            scope: Internal scope of landings;

            additional: Additional save parameters;

            prevent_history: If true is passed, the method will not add the change to the page history;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "lid": lid,
            "block": block,
            "data": data,
        }

        if scope is not MISSING:
            params["scope"] = scope

        if additional is not MISSING:
            params["additional"] = additional

        if prevent_history is not MISSING:
            params["preventHistory"] = bool_to_bitrix(prevent_history, is_required=True)

        return self._make_bitrix_api_request(
            api_wrapper=self.updatenodes,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def uploadfile(
            self,
            block: int,
            picture: Union[Text, Sequence[Text]],
            *,
            scope: Optional[Text] = MISSING,
            ext: Optional[Text] = MISSING,
            params: Optional[JSONDict] = MISSING,
            temp: Optional[bool] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Upload and attach an image to the block

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/block/methods/landing-block-upload-file.html

        The method uploads an image and attaches it to the specified block.

        Args:
            block: Identifier of the block in the editable version of the page;

            picture: Image to upload;

            scope: Internal scope of landings;

            ext: File extension for uploading via URL, if it cannot be accurately determined from the address;

            params: Additional parameters for image processing;

            temp: If the value is cast to true, the file is marked as temporary;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        if isinstance(picture, str):
            bitrix_picture = picture
        else:
            bitrix_picture = B24File(picture).to_b24()

        api_params: JSONDict = {
            "block": block,
            "picture": bitrix_picture,
        }

        if scope is not MISSING:
            api_params["scope"] = scope

        if ext is not MISSING:
            api_params["ext"] = ext

        if params is not MISSING:
            api_params["params"] = params

        if temp is not MISSING:
            api_params["temp"] = temp

        return self._make_bitrix_api_request(
            api_wrapper=self.uploadfile,
            params=api_params,
            timeout=timeout,
        )
