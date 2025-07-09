from typing import List, Optional, Text

from ...utils.types import B24BatchRequestData, JSONDict, JSONList, Timeout
from .call_batches import call_batches
from .call_method import call_method

STEP = 50
HALT = True


def _unwrap_result(result: JSONDict) -> List:
	""""""

	while isinstance(result, dict):
		result = next(iter(result.values()))

	if isinstance(result, list):
		return result
	else:
		raise TypeError("API method is not list")


def _unwrap_batch_result(batch_result: JSONDict) -> List:
	""""""

	list_result = list()

	for result in batch_result["result"]["result"]:
		list_result.extend(_unwrap_result(result))

	return list_result


def _generate_methods_for_batch(
	total: int,
	next_step: int,
	api_method: Text,
	params: Optional[JSONDict] = None,
) -> List[B24BatchRequestData]:
	"""
	Generates list of methods, using call_list() api_method and params, adding pagination parameter
	Args:
		total: total number of list method's results
		next_step: index from which generation starts
		api_method: bitrix api method to call
		params: parameters of bitrix api method

	Returns:
		list of B24BatchRequestData, ready to be used by call_batches()
	"""

	if params is None:
		params = dict()

	methods: List[B24BatchRequestData] = list()

	while next_step < total:
		params = params | {"start": next_step}
		methods.append((api_method, params))
		next_step += STEP

	return methods


def call_list(
		*,
		domain: Text,
		auth_token: Text,
		is_webhook: bool,
		api_method: Text,
		params: Optional[JSONDict] = None,
		timeout: Timeout = None,
		**kwargs,
) -> JSONList:
	""""""

	response = call_method(
		domain=domain,
		auth_token=auth_token,
		is_webhook=is_webhook,
		api_method=api_method,
		params=params,
		timeout=timeout,
		**kwargs
	)

	result: List = _unwrap_result(response["result"])

	next_step = response.get("next")
	total = response.get("total") or 0

	if next_step:
		batch_result = call_batches(
			domain=domain,
			auth_token=auth_token,
			is_webhook=is_webhook,
			methods=_generate_methods_for_batch(
				total=total,
				next_step=next_step,
				api_method=api_method,
				params=params,
			),
			halt=HALT,
			timeout=timeout,
		)
		result.extend(_unwrap_batch_result(batch_result))

	return result
