import functools
import typing

__all__ = [
    "Classproperty",
    "type_checker",
]


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


def _is_valid_type(
        value: typing.Any,
        expected_type: typing.Type,
        param_name: typing.Text,
) -> bool:
    """"""

    if expected_type is typing.Any:
        return True

    origin_type = typing.get_origin(expected_type)
    args = typing.get_args(expected_type)

    if origin_type is typing.Union:
        return any(_is_valid_type(value, arg, param_name) for arg in args)

    if origin_type is typing.Literal:
        if value in args:
            return True
        else:
            raise TypeError(
                f"Argument {param_name!r} must be one of {', '.join(repr(arg) for arg in args)}, "
                f"but got {value!r}",
            )

    if origin_type is not None:
        return isinstance(value, origin_type)

    return isinstance(value, expected_type)


def _check_param(
        param_name: typing.Text,
        value: typing.Any,
        type_hints: typing.Dict[typing.Text, typing.Any],
):
    """"""

    expected_type = type_hints.get(param_name)

    if expected_type and not _is_valid_type(value, expected_type, param_name):
        raise TypeError(
            f"Argument {param_name!r} must be of type {expected_type!r}, not {type(value).__name__!r}",
        )


_T = typing.TypeVar("_T", bound=typing.Callable[..., typing.Any])


def type_checker(func: _T) -> _T:
    """"""

    type_hints = typing.get_type_hints(func)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        for param_index, arg in enumerate(args):
            param_name = func.__code__.co_varnames[param_index]
            _check_param(param_name, arg, type_hints)

        for param_name, arg in kwargs.items():
            _check_param(param_name, arg, type_hints)

        return func(*args, **kwargs)

    return wrapper
