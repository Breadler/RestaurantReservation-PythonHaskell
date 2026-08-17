"""Search, filter, and reporting over reservations."""

from typing import List

from reservation import Reservation


# --- Search --------------------------------------------------------------

def search_by_customer(reservations: List[Reservation], customer_id: int) -> List[Reservation]:
    """Return all reservations for a given customer."""
    return [
    reservation
    for reservation in reservations
    if reservation.customer_id == customer_id
]


def filter_by_date(reservations: List[Reservation], date: str) -> List[Reservation]:
    """Return all reservations on a given date."""
    return [
    reservation
    for reservation in reservations
    if reservation.date == date
]


def filter_by_status(reservations: List[Reservation], status: str) -> List[Reservation]:
    """Return reservations matching the given status."""
    return [
        reservation
        for reservation in reservations
        if reservation.status.lower() == status.lower()
    ]


# --- Reporting -------------------------------------------------------------

def daily_summary(reservations: List[Reservation], date: str) -> dict:
    """Return total reservations and total guests for a given date."""
    daily_reservations = filter_by_date(reservations, date)

    return {
        "date": date,
        "total_reservations": len(daily_reservations),
        "total_guests": sum(
            reservation.party_size
            for reservation in daily_reservations
        )
    }


def sort_by_time(reservations: List[Reservation]) -> List[Reservation]:
    """Return reservations sorted by date and time."""
    return sorted(
        reservations,
        key=lambda reservation: (
            reservation.date,
            reservation.time
        )
    )
