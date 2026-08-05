"""Shared input validation helpers. Owner: whole group.

Each manager should call these before creating/updating a record and
surface a clear error message to the CLI layer on failure.
"""

from datetime import date, datetime


class ValidationError(ValueError):
    """Raised when user input fails validation."""


def validate_non_empty_string(value: str, field_name: str) -> str:
    """Raise ValidationError if `value` is empty/whitespace; else return it stripped."""
    raise NotImplementedError


def validate_phone(value: str) -> str:
    """Raise ValidationError if `value` isn't a plausible phone number."""
    raise NotImplementedError


def validate_email(value: str) -> str:
    """Raise ValidationError if `value` isn't a plausible email address."""
    raise NotImplementedError


def validate_date(value: str) -> str:
    """Raise ValidationError if `value` isn't a valid YYYY-MM-DD date, or is in the past."""
    value = value.strip()
    try:
        parsed = datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        raise ValidationError(f"'{value}' is not a valid date (expected YYYY-MM-DD).")
    if parsed < date.today():
        raise ValidationError(f"Reservation date {value} is in the past.")
    return value


def validate_time(value: str) -> str:
    """Raise ValidationError if `value` isn't a valid HH:MM 24-hour time."""
    value = value.strip()
    try:
        datetime.strptime(value, "%H:%M")
    except ValueError:
        raise ValidationError(f"'{value}' is not a valid time (expected HH:MM, 24-hour).")
    return value


def validate_party_size(value: int) -> int:
    """Raise ValidationError if `value` isn't a positive whole number."""
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValidationError("Party size must be a whole number.")
    if value <= 0:
        raise ValidationError("Party size must be at least 1.")
    return value
