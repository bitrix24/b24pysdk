from typing import Annotated, Literal, Optional, Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Engine",
]


class Engine(BaseEntity):
    """Handle operations related to Bitrix24 AI engines.

    Documentation: https://apidocs.bitrix24.com/api-reference/ai/index.html
    """

    @type_checker
    def list(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Retrieve the list of registered AI engines.

        Documentation: https://apidocs.bitrix24.com/api-reference/ai/ai-engine-list.html

        This method returns the list of engines registered for the current partner. The API call does not require parameters.

        Args:
            timeout: Timeout in seconds;
        Returns:
            Instance of BitrixAPIRequest.
        """
        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            timeout=timeout,
        )

    @type_checker
    def register(
            self,
            name: Text,
            code: Text,
            category: Annotated[Text, Literal["text", "image", "audio"]],
            completions_url: Text,
            *,
            settings: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Register an AI engine.

        Documentation: https://apidocs.bitrix24.com/api-reference/ai/ai-engine-register.html

        Registers a new engine. If the engine with the same code already exists, the API updates it.

        Args:
            name: Human-readable name shown in the user interface;

            code: Unique code of the engine;

            category: Engine category: 'text' (text generation), 'image' (image generation), or 'audio' (speech recognition);

            completions_url: Endpoint that processes completion requests;

            settings: Optional settings for the engine;

            timeout: Timeout in seconds;
        Returns:
            Instance of BitrixAPIRequest.
        """

        params = dict(
            name=name,
            code=code,
            category=category,
            completions_url=completions_url,
        )

        if settings is not None:
            params["settings"] = settings

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
        """Delete an AI engine by code.

        Documentation: https://apidocs.bitrix24.com/api-reference/ai/ai-engine-unregister.html

        This method removes the engine identified by the provided code.

        Args:
            code: Engine code to remove;

            timeout: Timeout in seconds;

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = dict(
            code=code,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.unregister,
            params=params,
            timeout=timeout,
        )
