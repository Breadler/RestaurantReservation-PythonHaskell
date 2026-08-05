"""Table model + availability/assignment manager. Owner: Member 3.

See docs/modules/table.md for design notes, implementation write-up, and
test cases this module feeds into.
"""

from dataclasses import dataclass
from typing import Dict, List

from reservation import Reservation


@dataclass
class Table:
    id: int
    capacity: int


class TableManager:
    def __init__(self) -> None:
        self._tables: Dict[int, Table] = {}
        self._next_id: int = 1

    def add_table(self, capacity: int) -> Table:
        """Register a new table."""
        raise NotImplementedError

    def list_available(
        self, date: str, time: str, reservations: List[Reservation]
    ) -> List[Table]:
        """Return tables with no active reservation at the given date/time.

        TODO(Member 3): a table is available if no reservation in
        `reservations` has status "active" with the same table_id, date,
        and time. Availability is computed from reservations rather than a
        stored flag on Table, so the two can never get out of sync.
        """
        raise NotImplementedError

    def is_double_booked(
        self, table_id: int, date: str, time: str, reservations: List[Reservation]
    ) -> bool:
        """Return True if the table already has an active reservation at
        the given date/time.

        TODO(Member 3): this is the core invariant enforced before
        ReservationManager.create()/update() assigns a table.
        """
        raise NotImplementedError

    def list_all(self) -> List[Table]:
        """Return all tables."""
        raise NotImplementedError
