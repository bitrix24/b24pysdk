from abc import ABC
from typing import Final, Iterable, List, Mapping, Optional, Text, Tuple

from ._base_caller import BaseCaller

__all__ = [
    "BaseListCaller",
]


class BaseListCaller(BaseCaller, ABC):
    """Base caller for list methods that optimize explicit ID filters.

    Subclasses define which non-filter parameters are compatible with their
    ID-only request strategy. The shared inspection logic supports both nested
    ``filter`` mappings and top-level filters used by methods such as
    ``department.get``.
    """

    _HALT: Final[bool] = True
    _FILTER_ID_KEYS: Tuple[Text, ...] = ("id", "@id")
    _NON_FILTER_PARAMS_FOR_OPTIMIZATION_BY_ID: Tuple[Text, ...] = ("select",)

    __slots__ = ()

    def _check_filter_by_id_only(self) -> Tuple[Text, Text, Optional[List[int]]]:
        """Inspect an ID filter and determine whether it can use an optimized path.

        ``ID`` and ``@ID`` are matched case-insensitively. An empty ID iterable
        is returned as an empty list even when additional filters are present,
        because such a request cannot match any items. A non-empty list is
        returned only when all parameters are compatible with the subclass's
        ID-only strategy.

        Non-list iterables are materialized once. If additional filters require
        the regular request path, the materialized IDs are stored in a private
        copy of ``_params`` so an exhausted iterator is not sent to Bitrix24.

        Returns:
            A tuple containing the enclosing filter key, the actual ID key, and
            the ID state. The enclosing key is empty for a top-level ID filter.
            The state is ``None`` for the regular request path, an empty list
            for an immediate empty result, or a non-empty list for the ID-only
            optimization.
        """

        filter_key: Text = ""
        filter_id_key: Text = ""
        filter_ids: Optional[List[int]] = None

        for key in self._params:
            if key.lower() == "filter":
                filter_key = key

        # Some methods expose filters directly in the top-level parameters.
        filter_param = self._params.get(filter_key, self._params)

        allowed_params = (
            ("filter", *self._NON_FILTER_PARAMS_FOR_OPTIMIZATION_BY_ID)
            if filter_key else (*self._FILTER_ID_KEYS, *self._NON_FILTER_PARAMS_FOR_OPTIMIZATION_BY_ID)
        )

        allowed_filter_fields = self._FILTER_ID_KEYS if filter_key else allowed_params
        can_optimize_by_id = all(key.lower() in allowed_params for key in self._params)

        if isinstance(filter_param, Mapping):
            for filter_field in filter_param:
                filter_field_lower = filter_field.lower()

                if filter_field_lower in self._FILTER_ID_KEYS:
                    filter_id_key = filter_field

                can_optimize_by_id = can_optimize_by_id and filter_field_lower in allowed_filter_fields

            if filter_id_key:
                filter_id_value = filter_param[filter_id_key]

                if (
                        isinstance(filter_id_value, Iterable) and
                        not isinstance(filter_id_value, (str, bytes, bytearray, Mapping))
                ):
                    filter_id_value_is_list = isinstance(filter_id_value, list)
                    filter_ids = filter_id_value if filter_id_value_is_list else list(filter_id_value)

                    if filter_ids and not (can_optimize_by_id or filter_id_value_is_list):
                        # The regular path still needs the IDs after the
                        # iterator above has been consumed. Copy only the
                        # mappings whose values must be replaced.
                        materialized_params = (
                            {filter_key: dict(filter_param) | {filter_id_key: filter_ids}}
                            if filter_key else {filter_id_key: filter_ids}
                        )

                        self._params = self._params.copy()
                        self._params.update(materialized_params)

        # Preserve [] as the no-request marker. Only a non-empty ID collection
        # with incompatible filters must continue through the regular path.
        if filter_ids and not can_optimize_by_id:
            filter_ids = None

        return filter_key, filter_id_key, filter_ids
