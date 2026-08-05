"""Search, filter, and (optional) reporting over reservations. Owner: Member 4.

See docs/modules/search-reporting.md for design notes, implementation
write-up, and test cases this module feeds into.
"""

from typing import List

from reservation import Reservation


def search_by_customer(reservations: List[Reservation], customer_id: int) -> List[Reservation]:
    """Return all reservations for a given customer."""
    raise NotImplementedError


def filter_by_date(reservations: List[Reservation], date: str) -> List[Reservation]:
    """Return all reservations on a given date."""
    raise NotImplementedError


def filter_by_status(reservations: List[Reservation], status: str) -> List[Reservation]:
    """Return all reservations with a given status ("active"/"cancelled")."""
    raise NotImplementedError


def daily_summary(reservations: List[Reservation], date: str) -> dict:
    """Optional: total reservations and total guests for a given date."""
    raise NotImplementedError


def sort_by_time(reservations: List[Reservation]) -> List[Reservation]:
    """Optional: return reservations sorted by date then time."""
    raise NotImplementedError
