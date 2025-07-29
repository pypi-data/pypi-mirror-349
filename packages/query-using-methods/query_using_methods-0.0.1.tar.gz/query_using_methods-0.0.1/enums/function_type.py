from enum import Enum


class FunctionType(Enum):
    """Common SQL function types."""

    LOWER = "LOWER"
    """Convert string to lowercase."""

    UPPER = "UPPER"
    """Convert string to uppercase."""

    SUBSTRING = "SUBSTRING"
    """Extract a substring from a string."""

    LENGTH = "LENGTH"
    """Get the length of a string."""

    CONCAT = "CONCAT"
    """Concatenate two or more strings."""

    ABS = "ABS"
    """Absolute value of a number."""

    ROUND = "ROUND"
    """Round a number to a specified number of decimal places."""

    DATE = "DATE"
    """Extract the date part from a timestamp."""

    TIME = "TIME"
    """Extract the time part from a timestamp."""

    COUNT = "COUNT"
    """Count the number of rows."""

    SUM = "SUM"
    """Calculate the sum of values."""

    AVG = "AVG"
    """Calculate the average of values."""

    MIN = "MIN"
    """Get the minimum value."""

    MAX = "MAX"
    """Get the maximum value."""
