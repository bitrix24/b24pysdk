from typing import Dict, List, Sequence, Text, Tuple, Union

from ...utils.types import B24BatchRequestData, JSONDict, JSONList, Key, Timeout
from .call_batch import call_batch

MAX_BATCH_SIZE = 50


def _force_dict(collection: Union[Dict, List]) -> JSONDict:
	"""
	Batch method can return its results in the form of either a dictionary or a list.
	This function converts results to dictionaries for uniformity.
	"""
	if isinstance(collection, dict):
		return collection
	else:
		return {str(index): element for index, element in enumerate(collection)}


def call_batches(
		domain: Text,
		auth_token: Text,
		is_webhook: bool,
		methods: Union[Dict[Key, B24BatchRequestData], Sequence[B24BatchRequestData]],
		halt: bool = False,
		timeout: Timeout = None,
		**kwargs,
) -> JSONDict:
	""""""

	if len(methods) <= MAX_BATCH_SIZE:
		return call_batch(
				domain=domain,
				auth_token=auth_token,
				is_webhook=is_webhook,
				methods=methods,
				halt=halt,
				timeout=timeout,
				**kwargs,
		)

	if not isinstance(methods, dict):
		methods = dict(enumerate(methods))

	batch_responses: JSONList = list()
	flat_methods: List[Tuple[Key, B24BatchRequestData]] = list(methods.items())

	for index in range(0, len(methods), MAX_BATCH_SIZE):
		methods_chunk = dict(flat_methods[index:index + MAX_BATCH_SIZE])
		batch_response = call_batch(
				domain=domain,
				auth_token=auth_token,
				is_webhook=is_webhook,
				methods=methods_chunk,
				halt=halt,
				timeout=timeout,
				**kwargs,
		)
		batch_responses.append(batch_response)

		if halt and batch_response["result"]["result_error"]:
			break

	first_batch_response = batch_responses[0]
	last_batch_response = batch_responses[-1]

	combined_response = dict(
		result=dict(
			result=dict(),
			result_error=dict(),
			result_total=dict(),
			result_next=dict(),
			result_time=dict(),
		),
		time=dict(
			start=first_batch_response["time"]["start"],
			finish=last_batch_response["time"]["finish"],
			duration=0,
			processing=0,
			date_start=first_batch_response["time"]["date_start"],
			date_finish=last_batch_response["time"]["date_finish"],
			operating_reset_at=last_batch_response["time"]["operating_reset_at"],
			operating=last_batch_response["time"]["operating"],
		)
	)

	if last_batch_response["time"].get("operating_reset_at") is not None:
		combined_response["time"]["operating_reset_at"] = last_batch_response["time"]["operating_reset_at"]

	if last_batch_response["time"].get("operating") is not None:
		combined_response["time"]["operating"] = last_batch_response["time"]["operating"]

	for batch_response in batch_responses:
		result = batch_response["result"]
		time = batch_response["time"]

		for key in ("result", "result_error", "result_total", "result_next", "result_time"):
			combined_response["result"][key].update(_force_dict(result.get(key, {})))

		combined_response["time"]["duration"] += time["duration"]
		combined_response["time"]["processing"] += time["processing"]

	return combined_response
