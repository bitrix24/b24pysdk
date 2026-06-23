from ..utils import enum as _enum

__all__ = [
    "PersonalGender",
    "UserType",
]


class PersonalGender(_enum.StrEnum):
    """Bitrix24 personal gender value."""
    EMPTY = ""
    FEMALE = "F"
    MALE = "M"


class UserType(_enum.StrEnum):
    """"""
    EMAIL = "email"
    EMPLOYEE = "employee"
    EXTRANET = "extranet"
