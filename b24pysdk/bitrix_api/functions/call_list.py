from typing import Iterable, List, Optional, Text, Tuple

from ..._constants import MAX_BATCH_SIZE
from ...utils.types import B24BatchRequestData, JSONDict, JSONList, Timeout
from .call_batches import call_batches
from .call_method import call_method

_ALLOWED_PARAMS_FOR_OPTIMIZATION_BY_ID = ("filter", "select")
_HALT = True
_STEP = MAX_BATCH_SIZE


def _unwrap_result(result: JSONDict, api_method: Text) -> JSONList:
	""""""

	while isinstance(result, dict):
		result = next(iter(result.values()))

	if isinstance(result, list):
		return result
	else:
		raise TypeError(f"API method '{api_method}' is not a list method!")


def _unwrap_batch_result(batch_result: JSONDict, api_method: Text) -> JSONList:
	""""""

	result_list = list()

	if isinstance(batch_result["result"], dict):
		result_values = batch_result["result"].values()
	else:
		result_values = batch_result["result"]

	for result_value in result_values:
		result_list.extend(_unwrap_result(result_value, api_method))

	return result_list


def _generate_methods_for_batch(
	api_method: Text,
	params: JSONDict,
	next_step: int,
	total: int,
) -> List[B24BatchRequestData]:
	"""
	Generates list of methods, using call_list() api_method and params, adding pagination parameter
	Args:
		api_method: bitrix api method to call
		params: parameters of bitrix api method
		next_step: index from which generation starts
		total: total number of list method's results

	Returns:
		list of B24BatchRequestData, ready to be used by call_batches()
	"""

	methods: List[B24BatchRequestData] = list()

	for start in range(next_step, total, _STEP):
		page_params = params | {"start": start}
		methods.append((api_method, page_params))

	return methods


def _generate_filter_id_methods_for_batch(
	api_method: Text,
	params: JSONDict,
	filter_key: Text,
	filter_id_key: Text,
	filter_ids: List[int],
) -> List[B24BatchRequestData]:
	"""
	Generates list of methods, using call_list() api_method and params, slicing ids from filter parameter in chunks

	Returns:
		list of B24BatchRequestData, ready to be used by call_batches()
	"""

	methods: List[B24BatchRequestData] = list()

	for start in range(0, len(filter_ids), _STEP):
		id_chunk = filter_ids[start:start + _STEP]
		chunk_params = params | {filter_key: {filter_id_key: id_chunk}}
		methods.append((api_method, chunk_params))

	return methods


def _check_filter_by_id_only(params: JSONDict) -> Tuple[Text, Text, List[int]]:
	"""
	Checks if method params contain only single filter by list of ids

	Returns:
		key by which filter values can be accessed

		key by which list of ids in filter can be accessed

		list of ids to filter by if params satisfy the condition, otherwise None
	"""

	filter_key = ""
	filter_id_key = ""
	filter_ids = []

	if not params:
		return filter_key, filter_id_key, filter_ids

	for key in params:
		if key.lower() == "filter":
			filter_key = key

		if key.lower() not in _ALLOWED_PARAMS_FOR_OPTIMIZATION_BY_ID:
			return filter_key, filter_id_key, filter_ids

	if not (filter_key and isinstance(params[filter_key], dict)):
		return filter_key, filter_id_key, filter_ids

	for filter_field in params[filter_key]:
		if filter_field.lower() in ("id", "@id"):
			filter_id_key = filter_field
		else:
			return filter_key, filter_id_key, filter_ids

	filter_id_value = params[filter_key][filter_id_key]

	if isinstance(filter_id_value, Iterable) and not isinstance(filter_id_value, (str, bytes)):
		filter_ids = list(filter_id_value)

	return filter_key, filter_id_key, filter_ids


def _add_time(target_time: JSONDict, term_time: JSONDict):
	""""""

	target_time["finish"] = term_time["finish"]
	target_time["duration"] += term_time["duration"]
	target_time["processing"] += term_time["processing"]
	target_time["date_finish"] = term_time["date_finish"]

	if target_time.get("operating_reset_at") is not None:
		target_time["operating_reset_at"] = term_time["operating_reset_at"]

	if target_time.get("operating") is not None:
		target_time["operating"] = term_time["operating"]


def call_list(
		*,
		domain: Text,
		auth_token: Text,
		is_webhook: bool,
		api_method: Text,
		params: Optional[JSONDict] = None,
		limit: Optional[int] = None,
		timeout: Timeout = None,
		**kwargs,
) -> JSONDict:
	""""""

	if params is None:
		params = dict()

	filter_key, filter_id_key, filter_ids = _check_filter_by_id_only(params)

	if filter_ids:

		methods = _generate_filter_id_methods_for_batch(
			api_method=api_method,
			params=params,
			filter_key=filter_key,
			filter_id_key=filter_id_key,
			filter_ids=filter_ids,
		)

		batch_response = call_batches(
			domain=domain,
			auth_token=auth_token,
			is_webhook=is_webhook,
			methods=methods,
			halt=_HALT,
			timeout=timeout,
			**kwargs,
		)

		batch_response["result"] = _unwrap_batch_result(batch_response["result"], api_method)
		batch_response["total"] = len(batch_response["result"])

		return batch_response

	response = call_method(
		domain=domain,
		auth_token=auth_token,
		is_webhook=is_webhook,
		api_method=api_method,
		params=params,
		timeout=timeout,
		**kwargs,
	)

	result = _unwrap_result(response["result"], api_method)
	time = response["time"]

	next_step = response.get("next")

	total = response.get("total") or 0
	total = min(total, limit) if limit else total

	if next_step:
		batch_response = call_batches(
			domain=domain,
			auth_token=auth_token,
			is_webhook=is_webhook,
			methods=_generate_methods_for_batch(
				api_method=api_method,
				params=params,
				next_step=next_step,
				total=total,
			),
			halt=_HALT,
			timeout=timeout,
			**kwargs,
		)

		result.extend(_unwrap_batch_result(batch_response["result"], api_method))

		_add_time(time, batch_response["time"])

	return dict(
		result=result[:total],
		time=time,
		total=total,
	)
