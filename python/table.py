"""Table model and availability manager."""

from dataclasses import dataclass
from typing import Dict, List, Optional

from reservation import Reservation


# --- Model -------------------------------------------------------------

@dataclass
class Table:
    id: int
    capacity: int
    status: str = "Active"  # "Active" or "Under Maintenance"


# --- Manager -------------------------------------------------------------

class TableManager:
    def __init__(self) -> None:
        self._tables: Dict[int, Table] = {}
        self._next_id: int = 1

    def add_table(self, capacity: int) -> Table:
        """Register a new table."""
        table = Table(id=self._next_id, capacity=capacity)
        self._tables[self._next_id] = table
        self._next_id += 1
        return table

    def view(self, table_id: int) -> Optional[Table]:
        """Return a table by ID, or None if not found."""
        return self._tables.get(table_id)

    def update(self, table_id: int, **kwargs) -> Optional[Table]:
        """Update a table's capacity and/or status. Returns None if not found."""
        table = self._tables.get(table_id)
        if table is None:
            return None

        if "capacity" in kwargs:
            table.capacity = kwargs["capacity"]
        if "status" in kwargs:
            table.status = kwargs["status"]

        return table

    def list_available(
        self, date: str, time: str, reservations: List[Reservation]
    ) -> List[Table]:
        """Return tables with no active reservation at the given date/time."""
        return [
            table
            for table in self.list_all()
            if table.status == "Active"
            and not self.is_double_booked(table.id, date, time, reservations)
        ]

    def is_double_booked(
        self, table_id: int, date: str, time: str, reservations: List[Reservation]
    ) -> bool:
        """Return True if the table already has an active reservation at the given date/time."""
        return any(
            reservation.status == "active"
            and reservation.table_id == table_id
            and reservation.date == date
            and reservation.time == time
            for reservation in reservations
        )

    def list_all(self) -> List[Table]:
        """Return all tables."""
        return list(self._tables.values())
