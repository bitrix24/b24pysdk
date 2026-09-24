import typing

from ..utils import enum as _enum

__all__ = [
    "ListIBlockType",
    "ListIBlockTypeLiteral",
]


ListIBlockTypeLiteral = typing.Literal[
    "lists",
    "bitrix_processes",
    "lists_socnet",
]


class ListIBlockType(_enum.StrEnum):
    LISTS = "lists"
    BITRIX_PROCESSES = "bitrix_processes"
    LISTS_SOCNET = "lists_socnet"
