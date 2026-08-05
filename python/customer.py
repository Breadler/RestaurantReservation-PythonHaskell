"""Customer model + CRUD manager. Owner: Member 2.

See docs/modules/customer.md for design notes, implementation write-up,
and test cases this module feeds into.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class Customer:
    id: int
    name: str
    phone: str
    email: str


class CustomerManager:
    def __init__(self) -> None:
        self._customers: Dict[int, Customer] = {}
        self._next_id: int = 1

    def add(self, name: str, phone: str, email: str) -> Customer:
        """Create and store a new customer.

        TODO(Member 2): validate name/phone/email via validation.py before
        creating the record.
        """
        raise NotImplementedError

    def view(self, customer_id: int) -> Optional[Customer]:
        """Return the customer with the given ID, or None if not found."""
        raise NotImplementedError

    def update(self, customer_id: int, **fields) -> Optional[Customer]:
        """Update one or more fields on an existing customer."""
        raise NotImplementedError

    def delete(self, customer_id: int) -> bool:
        """Remove a customer. Returns True if a customer was deleted.

        TODO(Member 2): decide how this interacts with existing reservations
        for the deleted customer (block delete vs. cascade).
        """
        raise NotImplementedError

    def list_all(self) -> List[Customer]:
        """Return all customers."""
        raise NotImplementedError
