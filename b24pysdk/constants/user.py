from ..utils import enum as _enum

__all__ = [
    "PersonalGender",
    "UserType",
]


class PersonalGender(_enum.StrEnum):
    """"""
    FEMALE = "F"
    MALE = "M"
    EMPTY = ""


class UserType(_enum.StrEnum):
    """"""
    EMPLOYEE = "employee"
    EXTRANET = "extranet"
    EMAIL = "email"
