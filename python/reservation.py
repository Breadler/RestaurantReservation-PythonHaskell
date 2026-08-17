"""Reservation model and CRUD manager."""

from dataclasses import dataclass
from typing import Dict, List, Optional

from validation import ValidationError, validate_date, validate_party_size, validate_time

UPDATABLE_FIELDS = {"customer_id", "table_id", "date", "time", "party_size"}


# --- Model -------------------------------------------------------------

@dataclass
class Reservation:
    id: int
    customer_id: int
    table_id: int
    date: str  # YYYY-MM-DD
    time: str  # HH:MM (24-hour)
    party_size: int
    status: str = "active"  # "active" or "cancelled"


# --- Manager -------------------------------------------------------------

class ReservationManager:
    def __init__(self) -> None:
        self._reservations: Dict[int, Reservation] = {}
        self._next_id: int = 1

    def create(
        self,
        customer_id: int,
        table_id: int,
        date: str,
        time: str,
        party_size: int,
    ) -> Reservation:
        """Validate fields and create a new reservation."""
        date = validate_date(date)
        time = validate_time(time)
        party_size = validate_party_size(party_size)

        reservation = Reservation(
            id=self._next_id,
            customer_id=customer_id,
            table_id=table_id,
            date=date,
            time=time,
            party_size=party_size,
        )
        self._reservations[reservation.id] = reservation
        self._next_id += 1
        return reservation

    def view(self, reservation_id: int) -> Optional[Reservation]:
        """Return the reservation with the given ID, or None if not found."""
        return self._reservations.get(reservation_id)

    def update(self, reservation_id: int, **fields) -> Optional[Reservation]:
        """Update one or more fields on an existing reservation."""
        reservation = self._reservations.get(reservation_id)
        if reservation is None:
            return None

        unknown = set(fields) - UPDATABLE_FIELDS
        if unknown:
            raise ValidationError(f"Unknown field(s): {', '.join(sorted(unknown))}")

        if "date" in fields:
            fields["date"] = validate_date(fields["date"])
        if "time" in fields:
            fields["time"] = validate_time(fields["time"])
        if "party_size" in fields:
            fields["party_size"] = validate_party_size(fields["party_size"])

        for key, value in fields.items():
            setattr(reservation, key, value)
        return reservation

    def cancel(self, reservation_id: int) -> bool:
        """Mark a reservation as cancelled. Returns True if found."""
        reservation = self._reservations.get(reservation_id)
        if reservation is None:
            return False
        reservation.status = "cancelled"
        return True

    def list_all(self) -> List[Reservation]:
        """Return all reservations."""
        return list(self._reservations.values())
