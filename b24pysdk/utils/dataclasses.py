import typing

from .. import _constants

if typing.TYPE_CHECKING:
    from . import types as _types

__all__ = [
    "frozen_dataclass_kwargs",
]


def frozen_dataclass_kwargs(
        *,
        init: bool = True,
        repr: bool = True,
        eq: bool = True,
        order: bool = False,
        unsafe_hash: bool = False,
        frozen: bool = True,
        slots: typing.Optional[bool] = None,
) -> "_types.JSONDict":
    """
    Build keyword arguments for dataclasses.dataclass() with SDK-wide defaults.

    Usage:

        import dataclasses

        @dataclasses.dataclass(**frozen_dataclass_kwargs())
        class Example:
            ...

        @dataclasses.dataclass(**frozen_dataclass_kwargs(eq=False))
        class Example:
            ...

    Defaults:
        frozen: True.
        slots: True on Python 3.10+.
        slots: Not passed to dataclasses.dataclass() on Python 3.9,
            because the standard library does not support it there.

    Other arguments mirror dataclasses.dataclass().
    """

    kwargs: _types.JSONDict = {
        "init": init,
        "repr": repr,
        "eq": eq,
        "order": order,
        "unsafe_hash": unsafe_hash,
        "frozen": frozen,
    }

    if slots is not None:
        if _constants.PYTHON_VERSION >= (3, 10):
            kwargs["slots"] = slots

    elif _constants.PYTHON_VERSION >= (3, 10):
        kwargs["slots"] = True

    return kwargs
