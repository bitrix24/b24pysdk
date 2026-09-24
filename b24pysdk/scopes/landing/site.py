from typing import Iterable, Optional, Text, Union

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, JSONList, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Site",
]


class Site(BaseEntity):
    """Class manages creation and configuration of web pages.

    Documentation: https://apidocs.bitrix24.com/api-reference/landing/site/index.html
    """

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            scope: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add site

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/site/landing-site-add.html

        The method creates a new site and returns the identifier of the created site.

        Args:
            fields: Set of fields for the new site;

            scope: Internal scope of landings;

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
    def update(
            self,
            bitrix_id: int,
            fields: JSONDict,
            *,
            scope: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update site

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/site/landing-site-update.html

        The method updates the parameters of the site.

        Args:
            bitrix_id: Identifier of the site;

            fields: Set of fields to update the site;

            scope: Internal scope of landings;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
            "fields": fields,
        }

        if scope is not MISSING:
            params["scope"] = scope

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            bitrix_id: int,
            *,
            scope: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete site

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/site/landing-site-delete.html

        The method only deletes an empty site without pages.

        Args:
            bitrix_id: Site identifier;

            scope: Internal scope of landings;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
        }

        if scope is not MISSING:
            params["scope"] = scope

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get_list(
            self,
            *,
            scope: Optional[Text] = MISSING,
            params: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the list of sites

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/site/landing-site-get-list.html

        The method retrieves a list of sites based on the selection parameters.

        Args:
            scope: Internal scope of landings;

            params: Parameters for selecting sites;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        _params: JSONDict = {}

        if scope is not MISSING:
            _params["scope"] = scope

        if params is not MISSING:
            _params["params"] = params

        return self._make_bitrix_api_request(
            api_wrapper=self.get_list,
            params=_params or None,
            timeout=timeout,
        )

    @type_checker
    def get_preview(
            self,
            bitrix_id: int,
            *,
            scope: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get URL preview of the site

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/site/landing-site-get-preview.html

        The method returns the URL preview of the site's index page.

        Args:
            bitrix_id: Site identifier;

            scope: Internal scope of landings;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
        }

        if scope is not MISSING:
            params["scope"] = scope

        return self._make_bitrix_api_request(
            api_wrapper=self.get_preview,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get_public_url(
            self,
            bitrix_id: Union[int, Iterable[int]],
            *,
            scope: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get public URL of the site

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/site/landing-site-get-public-url.html

        The method returns the complete public URL of a site or multiple sites.

        Args:
            bitrix_id: Identifier of the site or an array of site identifiers;

            scope: Internal scope of landings;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        if bitrix_id.__class__ is not list and not isinstance(bitrix_id, int):
            bitrix_id = list(bitrix_id)

        params: JSONDict = {
            "id": bitrix_id,
        }

        if scope is not MISSING:
            params["scope"] = scope

        return self._make_bitrix_api_request(
            api_wrapper=self.get_public_url,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def mark_delete(
            self,
            bitrix_id: int,
            *,
            scope: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Mark the site as deleted

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/site/landing-site-mark-delete.html

        The method marks the site as deleted and moves it to the trash.

        Args:
            bitrix_id: Site identifier;

            scope: Internal scope of landings;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
        }

        if scope is not MISSING:
            params["scope"] = scope

        return self._make_bitrix_api_request(
            api_wrapper=self.mark_delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def mark_un_delete(
            self,
            bitrix_id: int,
            *,
            scope: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Restore site from recycle bin

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/site/landing-site-mark-undelete.html

        The method restores a site from the recycle bin and removes the deletion flag.

        Args:
            bitrix_id: Site identifier;

            scope: Internal scope of landings;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
        }

        if scope is not MISSING:
            params["scope"] = scope

        return self._make_bitrix_api_request(
            api_wrapper=self.mark_un_delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def publication(
            self,
            bitrix_id: int,
            *,
            scope: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Publish the site

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/site/landing-site-publication.html

        The method publishes the site and its pages.

        Args:
            bitrix_id: Site identifier;

            scope: Internal scope of landings;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
        }

        if scope is not MISSING:
            params["scope"] = scope

        return self._make_bitrix_api_request(
            api_wrapper=self.publication,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def unpublic(
            self,
            bitrix_id: int,
            *,
            scope: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Unpublishing a site

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/site/landing-site-unpublic.html

        The method unpublishes the site and its pages, deactivating the site.

        Args:
            bitrix_id: Site identifier;

            scope: Internal scope of landings;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
        }

        if scope is not MISSING:
            params["scope"] = scope

        return self._make_bitrix_api_request(
            api_wrapper=self.unpublic,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def set_rights(
            self,
            bitrix_id: Union[int, Text],
            *,
            rights: Union[JSONDict, JSONList] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Set access permissions

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/rights/extended-model/landing-site-set-rights.html

        The method sets access permissions in the advanced permission model for the specified site.

        Args:
            bitrix_id: Site identifier;

            rights: Object format:

                {
                    "access_code_1": ["operation_1", "operation_2"],

                    "access_code_2": ["operation_1"]
                }

                where:

                - access_code_n — access code

                - operation_n — operation code;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
        }

        if rights is not MISSING:
            params["rights"] = rights

        return self._make_bitrix_api_request(
            api_wrapper=self.set_rights,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get_rights(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get access permissions

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/rights/extended-model/landing-site-get-rights.html

        The method retrieves the list of permissions for the current user for the specified site.

        Args:
            bitrix_id: Site identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get_rights,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def getadditionalfields(
            self,
            bitrix_id: int,
            *,
            scope: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get additional fields of the site

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/site/landing-site-get-additional-fields.html

        The method retrieves additional fields of the site.

        Args:
            bitrix_id: Site identifier;

            scope: Internal scope of landings;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
        }

        if scope is not MISSING:
            params["scope"] = scope

        return self._make_bitrix_api_request(
            api_wrapper=self.getadditionalfields,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def add_folder(
            self,
            site_id: int,
            fields: JSONDict,
            *,
            scope: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add folder to site

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/site/landing-site-add-folder.html

        The method creates a folder in the specified site and returns the identifier of the created folder.

        Args:
            site_id: Site identifier;

            fields: Set of fields for the folder being created;

            scope: Internal scope of landings;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "siteId": site_id,
            "fields": fields,
        }

        if scope is not MISSING:
            params["scope"] = scope

        return self._make_bitrix_api_request(
            api_wrapper=self.add_folder,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update_folder(
            self,
            site_id: int,
            folder_id: int,
            fields: JSONDict,
            *,
            scope: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Change folder

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/site/landing-site-update-folder.html

        The method updates the parameters of a site folder.

        Args:
            site_id: Site identifier;

            folder_id: Folder identifier;

            fields: Set of fields for the folder being updated;

            scope: Internal scope of landings;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "siteId": site_id,
            "folderId": folder_id,
            "fields": fields,
        }

        if scope is not MISSING:
            params["scope"] = scope

        return self._make_bitrix_api_request(
            api_wrapper=self.update_folder,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get_folders(
            self,
            site_id: int,
            *,
            scope: Optional[Text] = MISSING,
            filter: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get site folders

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/site/landing-site-get-folders.html

        The method landing.site.getFolders returns a list of site folders.

        Args:
            site_id: Site identifier;

            scope: Internal scope of landings;

            filter: Filter by folder fields;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "siteId": site_id,
        }

        if scope is not MISSING:
            params["scope"] = scope

        if filter is not MISSING:
            params["filter"] = filter

        return self._make_bitrix_api_request(
            api_wrapper=self.get_folders,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def publication_folder(
            self,
            folder_id: int,
            *,
            scope: Optional[Text] = MISSING,
            mark: Optional[bool] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Publish the website folder

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/site/landing-site-publication-folder.html

        The method publishes the website folder and its chain of parent folders.

        Args:
            folder_id: Folder identifier;

            scope: Internal scope of landings;

            mark: Mark the folder as published;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "folderId": folder_id,
        }

        if scope is not MISSING:
            params["scope"] = scope

        if mark is not MISSING:
            params["mark"] = mark

        return self._make_bitrix_api_request(
            api_wrapper=self.publication_folder,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def un_public_folder(
            self,
            folder_id: int,
            *,
            scope: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Unpublish a website folder

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/site/landing-site-unpublic-folder.html

        The method unpublishes a website folder and its parent folder chain.

        Args:
            folder_id: Folder identifier;

            scope: Internal scope of the landing pages;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "folderId": folder_id,
        }

        if scope is not MISSING:
            params["scope"] = scope

        return self._make_bitrix_api_request(
            api_wrapper=self.un_public_folder,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def mark_folder_delete(
            self,
            bitrix_id: int,
            *,
            scope: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Mark a folder as deleted

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/site/landing-site-mark-folder-delete.html

        The method marks a folder as deleted and moves it to the trash.

        Args:
            bitrix_id: Folder identifier;

            scope: Internal scope of the landing pages;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
        }

        if scope is not MISSING:
            params["scope"] = scope

        return self._make_bitrix_api_request(
            api_wrapper=self.mark_folder_delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def mark_folder_un_delete(
            self,
            bitrix_id: int,
            *,
            scope: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Restore folder from recycle bin

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/site/landing-site-mark-folder-undelete.html

        The method restores a folder from the recycle bin and removes the deletion mark from this folder and the pages within it.

        Args:
            bitrix_id: Folder identifier;

            scope: Internal scope of the landing pages;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
        }

        if scope is not MISSING:
            params["scope"] = scope

        return self._make_bitrix_api_request(
            api_wrapper=self.mark_folder_un_delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def binding_to_menu(
            self,
            bitrix_id: int,
            menu_code: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Bind knowledge base to menu

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/embedding/knowledge-base/landing-site-binding-to-menu.html

        The method binds the Knowledge Base to the specified menu.

        Args:
            bitrix_id: Knowledge base identifier;

            menu_code: Menu code;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
            "menuCode": menu_code,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.binding_to_menu,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def unbinding_from_menu(
            self,
            bitrix_id: int,
            menu_code: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Unbind knowledge base from menu

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/embedding/knowledge-base/landing-site-unbinding-from-menu.html

        The method landing.site.unbindingFromMenu removes the binding of the Knowledge Base from the specified menu.

        Args:
            bitrix_id: Knowledge base identifier;

            menu_code: Menu code;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
            "menuCode": menu_code,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.unbinding_from_menu,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def binding_to_group(
            self,
            bitrix_id: int,
            group_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Bind to social network group

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/embedding/knowledge-base/landing-site-binding-to-group.html

        The method binds the Knowledge Base to a Social Network group.

        Args:
            bitrix_id: Knowledge base identifier;

            group_id: Identifier of the social network group;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
            "groupId": group_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.binding_to_group,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def unbinding_from_group(
            self,
            bitrix_id: int,
            group_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Unbind knowledge base from social network group

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/embedding/knowledge-base/landing-site-unbinding-from-group.html

        The method removes the binding of the Knowledge Base to a Social Network group.

        Args:
            bitrix_id: Knowledge base site identifier;

            group_id: Identifier of the social network group;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
            "groupId": group_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.unbinding_from_group,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def get_menu_bindings(
            self,
            *,
            menu_code: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get menu bindings

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/embedding/knowledge-base/landing-site-get-menu-bindings.html

        The method returns Knowledge Base bindings to the menu.

        Args:
            menu_code: Menu code for filtering;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if menu_code is not MISSING:
            params["menuCode"] = menu_code

        return self._make_bitrix_api_request(
            api_wrapper=self.get_menu_bindings,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def get_group_bindings(
            self,
            *,
            group_id: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get group bindings

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/embedding/knowledge-base/landing-site-get-group-bindings.html

        The method returns the bindings of Knowledge Bases to groups.

        Args:
            group_id: Identifier of the group for filtering;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if group_id is not MISSING:
            params["groupId"] = group_id

        return self._make_bitrix_api_request(
            api_wrapper=self.get_group_bindings,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def full_export(
            self,
            bitrix_id: int,
            *,
            params: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Exporting the site

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/site/landing-site-full-export.html

        The method exports the site and its pages into an array for subsequent import.

        Args:
            bitrix_id: Site identifier;

            params: Additional export parameters;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        _params: JSONDict = {
            "id": bitrix_id,
        }

        if params is not MISSING:
            _params["params"] = params

        return self._make_bitrix_api_request(
            api_wrapper=self.full_export,
            params=_params,
            timeout=timeout,
        )
