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

    def __get__(self, instance: typing.Any, owner: typing.Optional[typing.Type] = None):
        if self.fget is None:
            raise AttributeError("Unreadable attribute")

        owner = instance if isinstance(instance, type) else type(instance)
        return self.fget(owner)

    def __set__(self, instance: typing.Any, value: typing.Any):
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


_FT = typing.TypeVar("_FT", bound=typing.Callable[..., typing.Any])


class _TypeChecker:
    """
    Callable class that enforces runtime type checking for function arguments.
    Supports Annotated types with type-based metadata constraints.
    """

    _HandlerType = typing.Callable[[typing.Any, typing.Type, typing.Text], bool]

    __slots__ = ("_func",)

    def __init__(self, func: _FT):
        self._func = func

    def __get__(
            self,
            instance: typing.Any,
            owner: typing.Optional[typing.Type] = None,
    ):
        """Support instance methods via partial binding."""
        if instance is None:
            return self
        else:
            return functools.partial(self.__call__, instance)

    def __call__(self, *args, **kwargs):
        """Check argument types and call the wrapped function."""

        for index, arg in enumerate(args):
            param_name = self._func.__code__.co_varnames[index]
            self._check_param(arg, param_name)

        for param_name, arg in kwargs.items():
            self._check_param(arg, param_name)

        return self._func(*args, **kwargs)

    @property
    def _handlers(self) -> typing.Dict[typing.Any, _HandlerType]:
        """"""
        return {
            typing.Annotated: self._handle_annotated,
            typing.Any: self._handle_any,
            typing.Literal: self._handle_literal,
            typing.Union: self._handle_union,
        }

    @property
    def _type_hints(self) -> typing.Dict[typing.Text, typing.Any]:
        """"""
        return typing.get_type_hints(self._func, include_extras=True)

    def _check_param(
            self,
            value: typing.Any,
            param_name: typing.Text,
    ):
        """Validates a single parameter against its annotated type."""

        expected_type = self._type_hints.get(param_name)

        if expected_type and not self._is_valid_type(value, expected_type, param_name):
            raise TypeError(
                f"Argument {param_name!r} must be of type {expected_type!r}, not {type(value).__name__!r}",
            )

    def _is_valid_type(
            self,
            value: typing.Any,
            expected_type: typing.Type,
            param_name: typing.Text,
    ) -> bool:
        """Determine if a value matches its expected type, delegating to handlers."""

        origin_type = typing.get_origin(expected_type) or expected_type
        handler = self._handlers.get(origin_type)

        if handler:
            return handler(value, expected_type, param_name)
        else:
            return isinstance(value, origin_type)

    # ------------------------------------- Handlers -------------------------------------

    def _handle_annotated(
            self,
            value: typing.Any,
            expected_type: typing.Type,
            param_name: typing.Text,
    ) -> bool:
        """Handler for Annotated: check base type and meta-type constraints."""

        base_type, *metas = typing.get_args(expected_type)

        if not self._is_valid_type(value, base_type, param_name):
            return False

        expected_types = [meta for meta in metas if isinstance(meta, type) or typing.get_origin(meta) is not None]

        if expected_types and not any(self._is_valid_type(value, expected_type, param_name) for expected_type in expected_types):
            raise TypeError(
                f"Argument {param_name!r} must match one of type constraints "
                f"{', '.join(repr(expected_type) for expected_type in expected_types)}, but got {value!r}",
            )

        return True

    @staticmethod
    def _handle_any(*_) -> bool:
        """Handler for Any: always True."""
        return True

    @staticmethod
    def _handle_literal(
            value: typing.Any,
            expected_type: typing.Type,
            param_name: typing.Text,
    ) -> bool:
        """Handler for Literal: check if value is one of the allowed literals."""

        allowed_values = typing.get_args(expected_type)

        if value in allowed_values:
            return True

        raise TypeError(
            f"Argument {param_name!r} must be one of {', '.join(repr(allowed_value) for allowed_value in allowed_values)}, "
            f"but got {value!r}",
        )

    def _handle_union(
            self,
            value: typing.Any,
            expected_type: typing.Type,
            param_name: typing.Text,
    ) -> bool:
        """Handler for Union: check if value matches any type in the union."""
        expected_types = typing.get_args(expected_type)
        return any(self._is_valid_type(value, expected_type, param_name) for expected_type in expected_types)


def type_checker(func: _FT) -> _FT:
    """
    Decorator that enforces runtime type checking for function arguments.
    Fully supports Annotated types with type-based metadata constraints.
    """

    checker = _TypeChecker(func)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return checker(*args, **kwargs)

    return wrapper
