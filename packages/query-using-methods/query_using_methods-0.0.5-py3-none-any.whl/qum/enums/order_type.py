from enum import Enum


class OrderType(Enum):
    """SQL ORDER BY clause types."""

    ASC = "ASC"
    """Order in ascending order (A-Z, 1-9)."""

    DESC = "DESC"
    """Order in descending order (Z-A, 9-1)."""
