import functools
import typing

__all__ = [
    "classproperty",
    "type_checker",
]


class classproperty:  # noqa: N801
    """
    Descriptor for declaring class-level properties.

    Works similarly to the built-in ``property``, but passes the owning class
    to the getter and setter instead of an instance. The resulting attribute can
    be accessed directly from the class.
    """

    def __init__(self, method: typing.Optional[typing.Callable] = None):
        """
        Initialize a class property descriptor.

        Args:
            method: Optional getter method accepting the owning class as
                its only argument.
        """
        self.fget = method
        self.fset = None

    def __get__(self, instance: typing.Any, owner: typing.Optional[typing.Type] = None):
        """
        Return the computed class-level property value.

        Args:
            instance: Instance used for descriptor access, or ``None`` when
                accessed through the class.
            owner: Owner class provided by the descriptor protocol.

        Returns:
            Value returned by the registered getter.

        Raises:
            AttributeError: If getter is not defined.
        """

        if self.fget is None:
            raise AttributeError("Unreadable attribute")

        owner = instance if isinstance(instance, type) else type(instance)

        return self.fget(owner)

    def __set__(self, instance: typing.Any, value: typing.Any):
        """
        Set the class-level property value.

        Args:
            instance: Instance used for descriptor access.
            value: Value to pass to the registered setter.

        Raises:
            AttributeError: If setter is not defined.
        """

        if self.fset is None:
            raise AttributeError("Can't set attribute")

        cls = instance if isinstance(instance, type) else type(instance)

        return self.fset(cls, value)

    def getter(self, method: typing.Optional[typing.Callable] = None):
        """
        Register a getter method for the class property.

        Args:
            method: Getter method accepting the owning class as its only
                argument.

        Returns:
            This descriptor instance.
        """
        self.fget = method
        return self

    def setter(self, method: typing.Callable):
        """
        Register a setter method for the class property.

        Args:
            method: Setter method accepting the owning class and value.

        Returns:
            This descriptor instance.
        """
        self.fset = method
        return self


_FT = typing.TypeVar("_FT", bound=typing.Callable[..., typing.Any])


class _TypeChecker(typing.Generic[_FT]):
    """
    Runtime argument type checker for callable objects.

    Validates positional and keyword arguments against function annotations
    before calling the wrapped function. Supports standard types, ``Any``,
    ``Literal``, ``Union`` and ``Annotated`` with type-based metadata
    constraints.
    """

    _HandlerType = typing.Callable[[typing.Any, typing.Type, typing.Text], bool]

    __slots__ = ("_func",)

    _func: _FT

    def __init__(self, func: _FT):
        """
        Initialize the checker.

        Args:
            func: Function whose arguments should be checked at runtime.
        """
        self._func = func

    def __get__(
            self,
            instance: typing.Any,
            owner: typing.Optional[typing.Type] = None,
    ):
        """
        Support descriptor binding for instance methods.

        Args:
            instance: Instance used for method access.
            owner: Owner class provided by the descriptor protocol.

        Returns:
            This checker for class access, or a partially bound callable for
            instance access.
        """
        if instance is None:
            return self
        else:
            return functools.partial(self.__call__, instance)

    def __call__(self, *args, **kwargs):
        """
        Validate arguments and call the wrapped function.

        Args:
            *args: Positional arguments passed to the wrapped function.
            **kwargs: Keyword arguments passed to the wrapped function.

        Returns:
            Result returned by the wrapped function.

        Raises:
            TypeError: If any checked argument does not match its annotation.
        """

        for index, arg in enumerate(args):
            param_name = self._func.__code__.co_varnames[index]  # type: ignore[attr-defined]
            self._check_param(arg, param_name)

        for param_name, arg in kwargs.items():
            self._check_param(arg, param_name)

        return self._func(*args, **kwargs)

    @property
    def _handlers(self) -> typing.Dict[typing.Any, _HandlerType]:
        """
        Return special type handlers.

        Returns:
            Mapping of supported typing origins to validation handlers.
        """
        return {
            typing.Annotated: self._annotated_handler,
            typing.Any: self._any_handler,
            typing.Literal: self._literal_handler,
            typing.Union: self._union_handler,
        }

    @property
    def _type_hints(self) -> typing.Dict[typing.Text, typing.Any]:
        """
        Return resolved type hints for the wrapped function.

        Returns:
            Function annotations resolved with ``include_extras=True`` so
            ``Annotated`` metadata is preserved.
        """
        return typing.get_type_hints(self._func, include_extras=True)

    def _check_param(
            self,
            value: typing.Any,
            param_name: typing.Text,
    ):
        """
        Validate a single argument against its annotation.

        Args:
            value: Runtime argument value.
            param_name: Function parameter name.

        Raises:
            TypeError: If the value does not match the annotated type.
        """

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
        """
        Check whether a value matches the expected type.

        Args:
            value: Runtime argument value.
            expected_type: Annotation or runtime type to validate against.
            param_name: Function parameter name used in error messages.

        Returns:
            True if the value satisfies the expected type.
        """

        origin_type = typing.get_origin(expected_type) or expected_type
        handler = self._handlers.get(origin_type)

        if handler:
            return handler(value, expected_type, param_name)
        else:
            return isinstance(value, origin_type)

    # ------------------------------------- Handlers -------------------------------------

    def _annotated_handler(
            self,
            value: typing.Any,
            expected_type: typing.Type,
            param_name: typing.Text,
    ) -> bool:
        """
        Validate ``Annotated`` values.

        The base type is checked first. Any metadata item that is itself a type
        or a typing construct is treated as an additional type constraint.

        Args:
            value: Runtime argument value.
            expected_type: ``Annotated`` type annotation.
            param_name: Function parameter name used in error messages.

        Returns:
            True if the value satisfies the base type and metadata constraints.

        Raises:
            TypeError: If metadata type constraints are present and none match.
        """

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
    def _any_handler(*_) -> bool:
        """
        Validate ``Any`` values.

        Returns:
            Always True.
        """
        return True

    @staticmethod
    def _literal_handler(
            value: typing.Any,
            expected_type: typing.Type,
            param_name: typing.Text,
    ) -> bool:
        """
        Validate ``Literal`` values.

        Args:
            value: Runtime argument value.
            expected_type: ``Literal`` type annotation.
            param_name: Function parameter name used in error messages.

        Returns:
            True if the value is one of the allowed literal values.

        Raises:
            TypeError: If the value is not allowed by the literal annotation.
        """

        allowed_values = typing.get_args(expected_type)

        if value in allowed_values:
            return True

        raise TypeError(
            f"Argument {param_name!r} must be one of {', '.join(repr(allowed_value) for allowed_value in allowed_values)}, "
            f"but got {value!r}",
        )

    def _union_handler(
            self,
            value: typing.Any,
            expected_type: typing.Type,
            param_name: typing.Text,
    ) -> bool:
        """
        Validate ``Union`` values.

        Args:
            value: Runtime argument value.
            expected_type: ``Union`` type annotation.
            param_name: Function parameter name used in error messages.

        Returns:
            True if the value matches at least one type from the union.
        """
        expected_types = typing.get_args(expected_type)
        return any(self._is_valid_type(value, expected_type, param_name) for expected_type in expected_types)


def type_checker(func: _FT) -> _FT:
    """
    Decorate a function with runtime argument type checking.

    Args:
        func: Function whose arguments should be checked before execution.

    Returns:
        Wrapped function that validates annotated arguments at runtime.

    Raises:
        TypeError: If a checked argument does not match its annotation.
    """

    checker = _TypeChecker(func)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return checker(*args, **kwargs)

    return wrapper
