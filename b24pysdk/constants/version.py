import typing

from ..utils import enum as _enum

__all__ = [
    "API_V3_METHODS",
    "B24APIVersion",
]

# Bitrix REST methods available in API v3
API_V3_METHODS: typing.Final[typing.Tuple[typing.Text, ...]] = (
    "documentation",
    "humanresources.node.add",
    "humanresources.node.children",
    "humanresources.node.count",
    "humanresources.node.edit",
    "humanresources.node.field.get",
    "humanresources.node.field.list",
    "humanresources.node.get",
    "humanresources.node.list",
    "humanresources.node.member.add",
    "humanresources.node.member.move",
    "humanresources.node.member.remove",
    "humanresources.node.member.set",
    "humanresources.node.move",
    "humanresources.node.search",
    "main.eventlog.get",
    "main.eventlog.field.get",
    "main.eventlog.field.list",
    "main.eventlog.list",
    "main.eventlog.tail",
    "mail.mailbox.field.get",
    "mail.mailbox.field.list",
    "mail.mailbox.get",
    "mail.mailbox.list",
    "mail.mailbox.senders",
    "mail.message.createcalendarevent",
    "mail.message.createchat",
    "mail.message.createcrmactivity",
    "mail.message.createfeedpost",
    "mail.message.createtask",
    "mail.message.field.get",
    "mail.message.field.list",
    "mail.message.forward",
    "mail.message.get",
    "mail.message.list",
    "mail.message.movetofolder",
    "mail.message.removecrmactivity",
    "mail.message.reply",
    "mail.message.send",
    "mail.message.thread",
    "mail.recipient.field.get",
    "mail.recipient.field.list",
    "mail.recipient.listcontacts",
    "mail.recipient.listemployees",
    "rest.documentation.openapi",
    "rest.scope.list",
    "tasks.task.access.get",
    "tasks.task.access.field.get",
    "tasks.task.access.field.list",
    "tasks.task.add",
    "tasks.task.chat.message.send",
    "tasks.task.chat.message.field.get",
    "tasks.task.chat.message.field.list",
    "tasks.task.delete",
    "tasks.task.field.get",
    "tasks.task.field.list",
    "tasks.task.file.attach",
    "tasks.task.file.field.get",
    "tasks.task.file.field.list",
    "tasks.task.get",
    "tasks.task.list",
    "tasks.task.update",
)


class B24APIVersion(_enum.IntEnum):
    """"""
    V1 = 1
    V2 = 2
    V3 = 3
