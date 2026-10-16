from typing import Optional, Text, Union

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Head",
]


class Head(BaseEntity):
    """Class for saving supervisor's evaluation for the completed session.

    Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/index.html
    """

    @type_checker
    def vote(
            self,
            session_id: Union[int, Text],
            *,
            rating: Optional[Union[int, Text]] = MISSING,
            comment: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Rate employee performance in the dialog

        Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/sessions/imopenlines-session-head-vote.html

        The method saves the manager's reting and comment for a completed dialog.

        Args:
            session_id: Session identifier;

            rating: Manager's rating;

            comment: Manager's comment on the rating;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        if rating is MISSING and comment is MISSING:
            raise ValueError("Either rating or comment must be provided.")

        params = dict(
            SESSION_ID=session_id,
        )

        if rating is not MISSING:
            params["RATING"] = rating

        if comment is not MISSING:
            params["COMMENT"] = comment

        return self._make_bitrix_api_request(
            api_wrapper=self.vote,
            params=params,
            timeout=timeout,
        )
