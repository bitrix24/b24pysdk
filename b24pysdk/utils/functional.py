from functools import wraps
from types import FunctionType
from typing import Any, Callable, Optional, Type, Union, get_args, get_origin, get_type_hints


class Classproperty:
    """
    Decorator that converts a method with a single cls argument into a property
    that can be accessed directly from the class.
    """

    def __init__(self, method: Optional[FunctionType] = None):
        self.fget = method
        self.fset = None

    def __get__(self, instance, cls: Optional[Type] = None):
        if self.fget is None:
            raise AttributeError("Unreadable attribute")

        cls = instance if isinstance(instance, type) else type(instance)
        return self.fget(cls)

    def __set__(self, instance, value):
        if self.fset is None:
            raise AttributeError("Can't set attribute")

        cls = instance if isinstance(instance, type) else type(instance)
        return self.fset(cls, value)

    def getter(self, method: Optional[FunctionType] = None):
        self.fget = method
        return self

    def setter(self, method: FunctionType):
        self.fset = method
        return self


def type_checker(func: FunctionType) -> Callable:
    """"""

    type_hints = get_type_hints(func)

    def is_valid_type(value: Any, expected_type: Type) -> bool:
        if expected_type is Any:
            return True

        origin_type = get_origin(expected_type)
        args = get_args(expected_type)

        if origin_type is Union:
            return any(is_valid_type(value, arg) for arg in args)

        if origin_type is not None:
            return isinstance(value, origin_type)

        return isinstance(value, expected_type)

    @wraps(func)
    def wrapper(*args, **kwargs):
        for param_index, arg in enumerate(args):
            param_name = func.__code__.co_varnames[param_index]
            expected_type = type_hints.get(param_name)

            if expected_type and not is_valid_type(arg, expected_type):
                raise TypeError(f"Argument '{param_name}' must be of type {expected_type}, not {type(arg).__name__}")

        for param_name, arg in kwargs.items():
            expected_type = type_hints.get(param_name)

            if expected_type and not is_valid_type(arg, expected_type):
                raise TypeError(f"Argument '{param_name}' must be of type {expected_type}, not {type(arg).__name__}")

        return func(*args, **kwargs)

    return wrapper
