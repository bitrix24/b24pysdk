import functools
import typing

_T = typing.TypeVar("_T", bound=typing.Callable[..., typing.Any])


class Classproperty:
    """
    Decorator that converts a method with a single cls argument into a property
    that can be accessed directly from the class.
    """

    def __init__(self, method: typing.Optional[typing.Callable] = None):
        self.fget = method
        self.fset = None

    def __get__(self, instance, cls: typing.Optional[typing.Type] = None):
        if self.fget is None:
            raise AttributeError("Unreadable attribute")

        cls = instance if isinstance(instance, type) else type(instance)
        return self.fget(cls)

    def __set__(self, instance, value):
        if self.fset is None:
            raise AttributeError("Can't set attribute")

        cls = instance if isinstance(instance, type) else type(instance)
        return self.fset(cls, value)

    def getter(self, method: typing.Optional[typing.Callable] = None):
        self.fget = method
        return self

    def setter(self, method: typing.Callable):
        self.fset = method
        return self


def type_checker(func: _T) -> _T:
    """"""

    type_hints = typing.get_type_hints(func)

    def is_valid_type(value: typing.Any, expected_type: typing.Type) -> bool:
        if expected_type is typing.Any:
            return True

        origin_type = typing.get_origin(expected_type)
        args = typing.get_args(expected_type)

        if origin_type is typing.Union:
            return any(is_valid_type(value, arg) for arg in args)

        if origin_type is not None:
            return isinstance(value, origin_type)

        return isinstance(value, expected_type)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        for param_index, arg in enumerate(args):
            param_name = func.__code__.co_varnames[param_index]
            expected_type = type_hints.get(param_name)

            if expected_type and not is_valid_type(arg, expected_type):
                raise TypeError(f"Argument '{param_name}' must be of type '{expected_type}', not '{type(arg).__name__}'")

        for param_name, arg in kwargs.items():
            expected_type = type_hints.get(param_name)

            if expected_type and not is_valid_type(arg, expected_type):
                raise TypeError(f"Argument '{param_name}' must be of type '{expected_type}', not '{type(arg).__name__}'")

        return func(*args, **kwargs)

    return wrapper
