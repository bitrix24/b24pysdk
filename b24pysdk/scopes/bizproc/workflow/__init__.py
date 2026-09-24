from functools import cached_property
from typing import Iterable, Optional, Sequence, Text

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import DocumentType, JSONDict, Timeout
from ..._base_entity import BaseEntity
from .template import Template

__all__ = [
    "Workflow",
]


class Workflow(BaseEntity):
    """Class for managing workflows.

    Documentation: https://apidocs.bitrix24.com/api-reference/bizproc/index.html
    """

    @cached_property
    def template(self) -> Template:
        """"""
        return Template(self)

    @type_checker
    def start(
            self,
            template_id: int,
            document_id: Sequence[Text],
            *,
            parameters: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Start business process

        Documentation: https://apidocs.bitrix24.com/api-reference/bizproc/bizproc-workflow-start.html

        The method initiates a new business process.

        Args:
            template_id: Identifier of the business process template;

            document_id: Identifier of the document to start the business process;

            parameters: Values for the parameters of the business process template;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "TEMPLATE_ID": template_id,
            "DOCUMENT_ID": DocumentType(document_id).to_b24(),
        }

        if parameters is not MISSING:
            params["PARAMETERS"] = parameters

        return self._make_bitrix_api_request(
            api_wrapper=self.start,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def instances(
            self,
            *,
            select: Optional[Iterable[Text]] = MISSING,
            filter: Optional[JSONDict] = MISSING,
            order: Optional[JSONDict] = MISSING,
            start: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of running workflows

        Documentation: https://apidocs.bitrix24.com/api-reference/bizproc/bizproc-workflow-instances.html

        The method retrieves a list of running workflows.

        Args:
            select: An array containing the list of fields to select;

            filter: An object for filtering the list of running workflows;

            order: An object for sorting the list of running workflows;

            start: This parameter is used for managing pagination;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if select is not MISSING:
            if select.__class__ is not list:
                select = list(select)

            params["SELECT"] = select

        if filter is not MISSING:
            params["FILTER"] = filter

        if order is not MISSING:
            params["ORDER"] = order

        if start is not MISSING:
            params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.instances,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def kill(
            self,
            bitrix_id: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete running process

        Documentation: https://apidocs.bitrix24.com/api-reference/bizproc/bizproc-workflow-kill.html

        The method deletes the running workflow along with all process data.

        Args:
            bitrix_id: Identifier of the workflow;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "ID": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.kill,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def terminate(
            self,
            bitrix_id: Text,
            *,
            status: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Stop active workflow

        Documentation: https://apidocs.bitrix24.com/api-reference/bizproc/bizproc-workflow-terminate.html

        The method stops the specified workflow.

        Args:
            bitrix_id: Identifier of the workflow to be stopped;

            status: Set the status text;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "ID": bitrix_id,
        }

        if status is not MISSING:
            params["STATUS"] = status

        return self._make_bitrix_api_request(
            api_wrapper=self.terminate,
            params=params,
            timeout=timeout,
        )
