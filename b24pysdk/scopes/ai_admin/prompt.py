from typing import Annotated, Iterable, Literal, Optional, Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Prompt",
]


class Prompt(BaseEntity):
    """Handle operations related to Bitrix24 AI prompts.

    Documentation: https://apidocs.bitrix24.com/api-reference/ai/prompts/index.html
    """

    @type_checker
    def register(
            self,
            code: Text,
            prompt: Text,
            *,
            category: Optional[Iterable[Text]] = None,
            icon: Optional[Text] = None,
            parent_code: Optional[Text] = None,
            section: Optional[Annotated[Text, Literal["create", "edit"]]] = None,
            sort: Optional[int] = None,
            translate: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add a new AI prompt.

        Documentation: https://apidocs.bitrix24.com/api-reference/ai/prompts/ai-prompt-register.html

        This method adds a prompt for CoPilot. The code is immutable; to update a prompt, delete it and register again.

        Args:
            code: Unique code for the prompt. Must use the rest_ prefix; it is set once and cannot be changed. Updating is only possible via deletion and re-registration;

            prompt: Text of the prompt sent to the AI. Special formatting (markers and conditions) may be used;

            category: Category of placement where CoPilot is embedded. CoPilot can appear in various places in the product; optional;

            icon: Icon code; optional;

            parent_code: Code of the parent section. Must use the rest_ prefix; optional;

            section: Category in the prompts menu for visual grouping. Allowed values: "create" — Create from text; "edit" — Edit text. If not specified, the prompt is placed above these categories; optional;

            sort: Sorting order used to arrange items; optional;

            translate: Array of translations for different languages. Ideally, at least English (en) and the portal language are provided; optional;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "code": code,
            "prompt": prompt,
        }

        if category is not None:
            if category.__class__ is not list:
                category = list(category)

            params["category"] = category

        if icon is not None:
            params["icon"] = icon

        if parent_code is not None:
            params["parent_code"] = parent_code

        if section is not None:
            params["section"] = section

        if sort is not None:
            params["sort"] = sort

        if translate is not None:
            params["translate"] = translate

        return self._make_bitrix_api_request(
            api_wrapper=self.register,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def unregister(
            self,
            code: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Unregister (delete) an AI prompt.

        Documentation: https://apidocs.bitrix24.com/api-reference/ai/prompts/ai-prompt-unregister.html

        This method removes a prompt by its unique code.

        Args:
            code: Unique code of the prompt. Always uses the rest_ prefix and cannot be changed;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "code": code,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.unregister,
            params=params,
            timeout=timeout,
        )
