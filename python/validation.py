"""Shared input validation helpers, used by all three managers."""

from datetime import date, datetime


import re


class ValidationError(ValueError):
    """Raised when user input fails validation."""


# --- Customer fields -------------------------------------------------------

def validate_non_empty_string(value: str, field_name: str) -> str:
    """Raise ValidationError if `value` is empty/whitespace; else return it stripped."""
    if not isinstance(value, str):
        raise ValidationError(f"{field_name} must be a string.")
    stripped = value.strip()
    if not stripped:
        raise ValidationError(f"{field_name} cannot be empty.")
    return stripped


def validate_phone(value: str) -> str:
    """Raise ValidationError if `value` isn't a plausible phone number."""
    stripped = validate_non_empty_string(value, "Phone number")
    if not re.fullmatch(r"^\+?[\d\s\-\(\)]{7,20}$", stripped):
        raise ValidationError(f"'{value}' is not a valid phone number.")
    digits = re.sub(r"\D", "", stripped)
    if len(digits) < 7 or len(digits) > 15:
        raise ValidationError("Phone number must contain between 7 and 15 digits.")
    return stripped


def validate_email(value: str) -> str:
    """Raise ValidationError if `value` isn't a plausible email address."""
    stripped = validate_non_empty_string(value, "Email address")
    email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.fullmatch(email_pattern, stripped):
        raise ValidationError(f"'{value}' is not a valid email address.")
    return stripped


# --- Reservation fields ------------------------------------------------------

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
