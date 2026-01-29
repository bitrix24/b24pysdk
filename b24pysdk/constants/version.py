import typing

from ..utils import enum as _enum

__all__ = [
    "API_V3_METHODS",
    "B24APIVersion",
]

# Bitrix REST methods available in API v3
API_V3_METHODS: typing.Final[typing.Tuple[typing.Text, ...]] = (
    "documentation",
    "main.eventlog.get",
    "main.eventlog.list",
    "main.eventlog.tail",
    "rest.documentation.openapi",
    "rest.scope.list",
    "tasks.task.access.get",
    "tasks.task.add",
    "tasks.task.chat.message.send",
    "tasks.task.delete",
    "tasks.task.file.attach",
    "tasks.task.get",
    "tasks.task.update",
)


class B24APIVersion(_enum.IntEnum):
    """"""
    V1 = 1
    V2 = 2
    V3 = 3
