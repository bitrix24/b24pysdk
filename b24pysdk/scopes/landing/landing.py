from typing import Optional, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.converters import bool_to_bitrix
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Landing",
]


class Landing(BaseEntity):
    """Class for working with pages.

    Documentation: https://apidocs.bitrix24.com/api-reference/landing/page/methods/index.html
    """

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            scope: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add page or folder

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/page/methods/landing-landing-add.html

        The method adds a page or folder to the specified site and returns the identifier of the created object.

        Args:
            fields: Set of fields for the new page or folder;

            scope: Internal scope of the landing;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "fields": fields,
        }

        if scope is not MISSING:
            params["scope"] = scope

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def add_by_template(
            self,
            site_id: int,
            code: Text,
            *,
            scope: Optional[Text] = MISSING,
            fields: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add page by template

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/page/methods/landing-landing-add-by-template.html

        The method creates a page in the specified site based on the template code and returns the identifier of the created page.

        Args:
            site_id: Identifier of the site where the page needs to be created;

            code: Template code for the page;

            scope: Internal scope of landings;

            fields: Additional parameters for creating the page;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "siteId": site_id,
            "code": code,
        }

        if scope is not MISSING:
            params["scope"] = scope

        if fields is not MISSING:
            params["fields"] = fields

        return self._make_bitrix_api_request(
            api_wrapper=self.add_by_template,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def addblock(
            self,
            lid: int,
            fields: JSONDict,
            *,
            scope: Optional[Text] = MISSING,
            prevent_history: Optional[bool] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add block to page

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/page/block-methods/landing-landing-add-block.html

        The method adds a new block to the page and returns the identifier of the created block.

        Args:
            lid: Page identifier;

            fields: Set of parameters for the new block;

            scope: Internal scope of landings;

            prevent_history: If true, the method does not add the action to the page change history;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "lid": lid,
            "fields": fields,
        }

        if scope is not MISSING:
            params["scope"] = scope

        if prevent_history is not MISSING:
            params["preventHistory"] = bool_to_bitrix(prevent_history, is_required=True)

        return self._make_bitrix_api_request(
            api_wrapper=self.addblock,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def copy(
            self,
            lid: int,
            *,
            scope: Optional[Text] = MISSING,
            to_site_id: Optional[int] = MISSING,
            to_folder_id: Optional[int] = MISSING,
            skip_system: Optional[bool] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Copy page

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/page/methods/landing-landing-copy.html

        The method copies a page and returns the identifier of the new page.

        Args:
            lid: Identifier of the source page;

            scope: Internal scope of landings;

            to_site_id: Identifier of the target site;

            to_folder_id: Identifier of the target folder;

            skip_system: Flag for copying the system attribute of the page;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "lid": lid,
        }

        if scope is not MISSING:
            params["scope"] = scope

        if to_site_id is not MISSING:
            params["toSiteId"] = to_site_id

        if to_folder_id is not MISSING:
            params["toFolderId"] = to_folder_id

        if skip_system is not MISSING:
            params["skipSystem"] = bool_to_bitrix(skip_system, is_required=True)

        return self._make_bitrix_api_request(
            api_wrapper=self.copy,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def copyblock(
            self,
            lid: int,
            block: int,
            *,
            scope: Optional[Text] = MISSING,
            params: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Copy block to page

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/page/block-methods/landing-landing-copy-block.html

        The method copies a block to the specified page and returns the identifier of the created copy of the block.

        Args:
            lid: Identifier of the source page;

            block: Block identifier;

            scope: Internal scope of landings;

            params: Additional copy parameters;

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
            api_wrapper=self.copyblock,
            params=api_params or None,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            lid: int,
            *,
            scope: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete page

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/page/methods/landing-landing-delete.html

        The method removes a page along with its blocks and associated files.

        Args:
            lid: Identifier of the source page;

            scope: Internal scope of landings;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "lid": lid,
        }

        if scope is not MISSING:
            params["scope"] = scope

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def deleteblock(
            self,
            lid: int,
            block: int,
            *,
            scope: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete block

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/page/block-methods/landing-landing-delete-block.html

        The method landing.landing.deleteblock completely removes a block from the page.

        Args:
            lid: Identifier of the source page;

            block: Identifier of the block in the editable version of the page;

            scope: Internal scope of landings;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "lid": lid,
            "block": block,
        }

        if scope is not MISSING:
            params["scope"] = scope

        return self._make_bitrix_api_request(
            api_wrapper=self.deleteblock,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def downblock(
            self,
            lid: int,
            block: int,
            *,
            scope: Optional[Text] = MISSING,
            prevent_history: Optional[bool] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Move block down

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/page/block-methods/landing-landing-down-block.html

        The method moves a block one position down in the page draft.

        Args:
            lid: Identifier of the source page;

            block: Identifier of the block in the editable version of the page;

            scope: Internal scope of landings;

            prevent_history: If true, the method does not add the action to the page change history;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "lid": lid,
            "block": block,
        }

        if scope is not MISSING:
            params["scope"] = scope

        if prevent_history is not MISSING:
            params["preventHistory"] = bool_to_bitrix(prevent_history, is_required=True)

        return self._make_bitrix_api_request(
            api_wrapper=self.downblock,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def favorite_block(
            self,
            lid: int,
            block: int,
            *,
            scope: Optional[Text] = MISSING,
            meta: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Save to the list of blocks

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/page/block-methods/landing-landing-favorite-block.html

        The method creates a copy of a page block and saves it to the block list as a template.

        Args:
            lid: Identifier of the source page;

            block: Identifier of the block in the editable version of the page;

            scope: Internal scope of landings;

            meta: Parameters of the saved block;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "lid": lid,
            "block": block,
        }

        if scope is not MISSING:
            params["scope"] = scope

        if meta is not MISSING:
            params["meta"] = meta

        return self._make_bitrix_api_request(
            api_wrapper=self.favorite_block,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def getadditionalfields(
            self,
            lid: int,
            *,
            scope: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get additional fields of the page

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/page/methods/landing-landing-get-additional-fields.html

        The method retrieves additional fields of the page.

        Args:
            lid: Identifier of the source page;

            scope: Internal scope of landings;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "lid": lid,
        }

        if scope is not MISSING:
            params["scope"] = scope

        return self._make_bitrix_api_request(
            api_wrapper=self.getadditionalfields,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get_list(
            self,
            *,
            scope: Optional[Text] = MISSING,
            params: Optional[JSONDict] = MISSING,
            start: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of pages

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/page/methods/landing-landing-get-list.html

        The method retrieves a list of pages based on the selection parameters.

        Args:
            scope: Internal scope of the landings;

            params: Parameters for selecting pages;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        api_params: JSONDict = {}

        if scope is not MISSING:
            api_params["scope"] = scope

        if params is not MISSING:
            api_params["params"] = params

        if start is not MISSING:
            api_params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.get_list,
            params=api_params or None,
            timeout=timeout,
        )

    @type_checker
    def getpreview(
            self,
            lid: int,
            *,
            scope: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the URL of the preview

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/page/methods/landing-landing-get-preview.html

        The method returns the URL or relative path to the preview image of the page.

        Args:
            lid: Identifier of the source page;

            scope: Internal scope of the landings;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "lid": lid,
        }

        if scope is not MISSING:
            params["scope"] = scope

        return self._make_bitrix_api_request(
            api_wrapper=self.getpreview,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def getpublicurl(
            self,
            lid: int,
            *,
            scope: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get public URL of the page

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/page/methods/landing-landing-get-public-url.html

        The method returns the complete public URL of the page.

        Args:
            lid: Identifier of the source page;

            scope: Internal scope of the landings;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "lid": lid,
        }

        if scope is not MISSING:
            params["scope"] = scope

        return self._make_bitrix_api_request(
            api_wrapper=self.getpublicurl,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def hideblock(
            self,
            lid: int,
            block: int,
            *,
            scope: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Hide block on page

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/page/block-methods/landing-landing-hide-block.html

        The method hides a block on the page.

        Args:
            lid: Identifier of the source page;

            block: Identifier of the block in the editable version of the page;

            scope: Internal scope of landings;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "lid": lid,
            "block": block,
        }

        if scope is not MISSING:
            params["scope"] = scope

        return self._make_bitrix_api_request(
            api_wrapper=self.hideblock,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def mark_delete(
            self,
            lid: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Mark page as deleted

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/page/methods/landing-landing-mark-delete.html

        The method landing.landing.markDelete marks the page as deleted, moves it to the trash, and unpublishes it.

        Args:
            lid: Identifier of the source page;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "lid": lid,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.mark_delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def mark_deleted_block(
            self,
            lid: int,
            block: int,
            *,
            scope: Optional[Text] = MISSING,
            mark: Optional[bool] = MISSING,
            prevent_history: Optional[bool] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Mark block as deleted

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/page/block-methods/landing-landing-mark-deleted-block.html

        The method  marks a page block as deleted but does not remove it from the database.

        Args:
            lid: Identifier of the source page;

            block: Identifier of the block in the editable version of the page;

            scope: Internal scope of landings;

            mark: Indicator for marking the block as deleted;

            prevent_history: If true, the method does not add the action to the page change history;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "lid": lid,
            "block": block,
        }

        if scope is not MISSING:
            params["scope"] = scope

        if mark is not MISSING:
            params["mark"] = bool_to_bitrix(mark, is_required=True)

        if prevent_history is not MISSING:
            params["preventHistory"] = bool_to_bitrix(prevent_history, is_required=True)

        return self._make_bitrix_api_request(
            api_wrapper=self.mark_deleted_block,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def mark_un_delete(
            self,
            lid: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Restore page from recycle bin

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/page/methods/landing-landing-mark-undelete.html

        The method restores a page from the recycle bin and removes the deletion flag.

        Args:
            lid: Identifier of the source page;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "lid": lid,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.mark_un_delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def mark_undeleted_block(
            self,
            lid: int,
            block: int,
            *,
            scope: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Remove the deletion mark from block

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/page/block-methods/landing-landing-mark-undeleted-block.html

        The method removes the deletion mark from the block.

        Args:
            lid: Identifier of the source page;

            block: Identifier of the block in the editable version of the page;

            scope: Internal scope of landings;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "lid": lid,
            "block": block,
        }

        if scope is not MISSING:
            params["scope"] = scope

        return self._make_bitrix_api_request(
            api_wrapper=self.mark_undeleted_block,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def move(
            self,
            lid: int,
            *,
            scope: Optional[Text] = MISSING,
            to_site_id: Optional[int] = MISSING,
            to_folder_id: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Move page

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/page/methods/landing-landing-move.html

        The method moves a page to another site or folder.

        Args:
            lid: Identifier of the source page;

            scope: Internal scope of landings;

            to_site_id: Identifier of the target site;

            to_folder_id: Identifier of the target folder;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "lid": lid,
        }

        if scope is not MISSING:
            params["scope"] = scope

        if to_site_id is not MISSING:
            params["toSiteId"] = to_site_id

        if to_folder_id is not MISSING:
            params["toFolderId"] = to_folder_id

        return self._make_bitrix_api_request(
            api_wrapper=self.move,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def moveblock(
            self,
            lid: int,
            block: int,
            *,
            scope: Optional[Text] = MISSING,
            params: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Move block to page

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/page/block-methods/landing-landing-move-block.html

        The method moves a block to the specified page and returns the identifier of the moved block.

        Args:
            lid: Identifier of the source page;

            block: Identifier of the block in the editable version of the page;

            scope: Internal scope of landings;

            params: Additional parameters for the move;

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
            api_wrapper=self.moveblock,
            params=api_params or None,
            timeout=timeout,
        )

    @type_checker
    def publication(
            self,
            lid: int,
            *,
            scope: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Publish the landing page

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/page/methods/landing-landing-publication.html

        The method publishes the page and makes it active.

        Args:
            lid: Identifier of the source page;

            scope: Internal scope of landings;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "lid": lid,
        }

        if scope is not MISSING:
            params["scope"] = scope

        return self._make_bitrix_api_request(
            api_wrapper=self.publication,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def remove_entities(
            self,
            lid: int,
            data: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Remove blocks and clear image file bindings on page

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/page/methods/landing-landing-remove-entities.html

        The method removes specified blocks and their associated images from the page.

        Args:
            lid: Identifier of the source page;

            data: Set of objects to be deleted;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "lid": lid,
            "data": data,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.remove_entities,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def resolve_id_by_public_url(
            self,
            landing_url: Text,
            site_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get page ID by public URL

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/page/methods/landing-landing-resolve-id-by-public-url.html

        The method returns the page ID based on its public URL within the specified site.

        Args:
            landing_url: Relative public URL of the page within the site siteId;

            site_id: The ID of the site within which to find the page;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "landingUrl": landing_url,
            "siteId": site_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.resolve_id_by_public_url,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def showblock(
            self,
            lid: int,
            block: int,
            *,
            scope: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Show block on page

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/page/block-methods/landing-landing-show-block.html

        The method displays a block on the page that was previously hidden.

        Args:
            lid: Identifier of the source page;

            block: Identifier of the block in the editable version of the page;

            scope: Internal scope of landings;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "lid": lid,
            "block": block,
        }

        if scope is not MISSING:
            params["scope"] = scope

        return self._make_bitrix_api_request(
            api_wrapper=self.showblock,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def un_favorite_block(
            self,
            block_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Remove from the saved list of blocks

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/page/block-methods/landing-landing-unfavorite-block.html

        The method removes the saved copy of a block.

        Args:
            block_id: Identifier of the saved copy of the block;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "blockId": block_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.un_favorite_block,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def unpublic(
            self,
            lid: int,
            *,
            scope: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Unpublishing the page

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/page/methods/landing-landing-unpublic.html

        The method unpublishes a page.

        Args:
            lid: Identifier of the source page;

            scope: Internal scope of landings;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "lid": lid,
        }

        if scope is not MISSING:
            params["scope"] = scope

        return self._make_bitrix_api_request(
            api_wrapper=self.unpublic,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            lid: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update page

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/page/methods/landing-landing-update.html

        The method updates the parameters of the page.

        Args:
            lid: Identifier of the source page;

            fields: A set of fields for the page to be updated;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "lid": lid,
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def upblock(
            self,
            lid: int,
            block: int,
            *,
            scope: Optional[Text] = MISSING,
            prevent_history: Optional[bool] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Move block up

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/page/block-methods/landing-landing-up-block.html

        The method moves a block one position up in the draft of the page.

        Args:
            lid: Identifier of the source page;

            block: Identifier of the block in the editable version of the page;

            scope: Internal scope of landings;

            prevent_history: If true, the method does not add the action to the page change history;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "lid": lid,
            "block": block,
        }

        if scope is not MISSING:
            params["scope"] = scope

        if prevent_history is not MISSING:
            params["preventHistory"] = bool_to_bitrix(prevent_history, is_required=True)

        return self._make_bitrix_api_request(
            api_wrapper=self.upblock,
            params=params,
            timeout=timeout,
        )
