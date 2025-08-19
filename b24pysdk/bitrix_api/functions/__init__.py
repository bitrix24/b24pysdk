from ...utils.functional import type_checker
from .call import call
from .call_batch import call_batch
from .call_batches import call_batches
from .call_list import call_list
from .call_list_fast import call_list_fast
from .call_method import call_method

call = type_checker(call)
call_batch = type_checker(call_batch)
call_batches = type_checker(call_batches)
call_list = type_checker(call_list)
call_list_fast = type_checker(call_list_fast)
call_method = type_checker(call_method)

__all__ = [
    "call",
    "call_batch",
    "call_batches",
    "call_list",
    "call_list_fast",
    "call_method",
]
