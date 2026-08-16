"""Table model + availability/assignment manager. Owner: Member 3.

See docs/modules/table.md for design notes, implementation write-up, and
test cases this module feeds into.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional

from reservation import Reservation


@dataclass
class Table:
    id: int
    capacity: int
    status: str = "Active"  # "Active" or "Under Maintenance"


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
        """Update a table's attributes (e.g., capacity or status).

        Supported kwargs:
        - capacity: int
        - status: str

        Returns the updated table, or None if not found.
        """
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
        """Return tables with no active reservation at the given date/time.

        Availability is computed from the reservations list instead of a
        stored booking flag, so table state and reservation state cannot fall
        out of sync.
        """
        return [
            table
            for table in self.list_all()
            if table.status == "Active"
            and not self.is_double_booked(table.id, date, time, reservations)
        ]

    def is_double_booked(
        self, table_id: int, date: str, time: str, reservations: List[Reservation]
    ) -> bool:
        """Return True if the table already has an active reservation at
        the given date/time.

        This is the core invariant enforced before a reservation is created or
        updated.
        """
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
