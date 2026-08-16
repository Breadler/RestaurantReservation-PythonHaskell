"""Customer model + CRUD manager. Owner: Member 2.

See docs/modules/customer.md for design notes, implementation write-up,
and test cases this module feeds into.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional

from validation import (
    ValidationError,
    validate_email,
    validate_non_empty_string,
    validate_phone,
)

UPDATABLE_FIELDS = {"name", "phone", "email"}


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
        """Create and store a new customer after validating fields."""
        name = validate_non_empty_string(name, "Customer name")
        phone = validate_phone(phone)
        email = validate_email(email)

        customer = Customer(
            id=self._next_id,
            name=name,
            phone=phone,
            email=email,
        )
        self._customers[customer.id] = customer
        self._next_id += 1
        return customer

    def view(self, customer_id: int) -> Optional[Customer]:
        """Return the customer with the given ID, or None if not found."""
        return self._customers.get(customer_id)

    def update(self, customer_id: int, **fields) -> Optional[Customer]:
        """Update one or more fields on an existing customer."""
        customer = self._customers.get(customer_id)
        if customer is None:
            return None

        unknown = set(fields) - UPDATABLE_FIELDS
        if unknown:
            raise ValidationError(f"Unknown field(s): {', '.join(sorted(unknown))}")

        if "name" in fields:
            fields["name"] = validate_non_empty_string(fields["name"], "Customer name")
        if "phone" in fields:
            fields["phone"] = validate_phone(fields["phone"])
        if "email" in fields:
            fields["email"] = validate_email(fields["email"])

        for key, value in fields.items():
            setattr(customer, key, value)
        return customer

    def delete(self, customer_id: int) -> bool:
        """Remove a customer. Returns True if a customer was deleted."""
        if customer_id in self._customers:
            del self._customers[customer_id]
            return True
        return False

    def list_all(self) -> List[Customer]:
        """Return all customers."""
        return list(self._customers.values())
