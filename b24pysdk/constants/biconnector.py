from ..utils import enum as _enum

__all__ = [
    "BiconnectorDatasetFieldType",
]


class BiconnectorDatasetFieldType(_enum.StrEnum):
    """Field types supported by biconnector.dataset.add fields[].type."""
    INT = "int"
    STRING = "string"
    DOUBLE = "double"
    DATE = "date"
    DATETIME = "datetime"

