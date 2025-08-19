from ......bitrix_api.classes import BitrixAPIRequest
from ......utils.functional import type_checker
from ......utils.types import Timeout
from ..detail import Detail
from .field import Field


class Preset(Detail):
    """The class provide methods for working with requisite templates.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/requisites/presets/index.html
    """

    @property
    def field(self) -> Field:
        """"""
        return Field(self)

    @type_checker
    def countries(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of countries for the template.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/requisites/presets/crm-requisite-preset-countries.html

        THe method returns a possible list of countries for requisite template.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._make_bitrix_api_request(
            api_method=self.countries,
            timeout=timeout,
        )
