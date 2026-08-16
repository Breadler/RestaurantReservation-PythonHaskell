"""Menu-driven entry point. Run with `python main.py` from inside python/."""

from customer import CustomerManager
from reservation import ReservationManager
from table import TableManager
from validation import ValidationError


def run() -> None:
    customers = CustomerManager()
    reservations = ReservationManager()
    tables = TableManager()

    actions = {
        "1": lambda: customer_menu(customers),
        "2": lambda: reservation_menu(reservations, tables, customers),
        "3": lambda: table_menu(tables, reservations),
        "4": lambda: search_menu(reservations),
    }

    while True:
        print("\n=== Restaurant Reservation System ===")
        print("1. Customers")
        print("2. Reservations")
        print("3. Tables")
        print("4. Search & Reports")
        print("5. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "5":
            print("Goodbye!")
            return

        action = actions.get(choice)
        if action is None:
            print("Invalid choice.")
            continue

        try:
            action()
        except NotImplementedError:
            print("This feature is not implemented yet.")
        except ValidationError as exc:
            print(f"Invalid input: {exc}")


def customer_menu(customers: CustomerManager) -> None:
    while True:
        print("\n--- Customers ---")
        print("1. Add customer")
        print("2. View customer")
        print("3. Update customer")
        print("4. Delete customer")
        print("5. List all customers")
        print("6. Back")
        choice = input("Choose an option: ").strip()

        try:
            if choice == "6":
                return
            elif choice == "1":
                _add_customer_prompt(customers)
            elif choice == "2":
                _view_customer_prompt(customers)
            elif choice == "3":
                _update_customer_prompt(customers)
            elif choice == "4":
                _delete_customer_prompt(customers)
            elif choice == "5":
                _list_customers_prompt(customers)
            else:
                print("Invalid choice.")
        except ValidationError as exc:
            print(f"Invalid input: {exc}")
        except NotImplementedError:
            print("That part isn't implemented yet (waiting on another module).")
        except ValueError:
            print("Please enter a whole number where one is expected.")


def _add_customer_prompt(customers: CustomerManager) -> None:
    name = input("Name: ").strip()
    phone = input("Phone: ").strip()
    email = input("Email: ").strip()
    customer = customers.add(name, phone, email)
    print(f"Added customer #{customer.id}: {customer.name}.")


def _view_customer_prompt(customers: CustomerManager) -> None:
    customer_id = int(input("Customer ID: ").strip())
    customer = customers.view(customer_id)
    print(customer if customer else "Not found.")


def _update_customer_prompt(customers: CustomerManager) -> None:
    customer_id = int(input("Customer ID: ").strip())
    field = input("Field to update (name/phone/email): ").strip()
    value = input("New value: ").strip()
    updated = customers.update(customer_id, **{field: value})
    print(updated if updated else "Not found.")


def _delete_customer_prompt(customers: CustomerManager) -> None:
    customer_id = int(input("Customer ID: ").strip())
    deleted = customers.delete(customer_id)
    print("Deleted." if deleted else "Not found.")


def _list_customers_prompt(customers: CustomerManager) -> None:
    all_customers = customers.list_all()
    if not all_customers:
        print("No customers yet.")
        return
    for customer in all_customers:
        print(customer)


def reservation_menu(
    reservations: ReservationManager,
    tables: TableManager,
    customers: CustomerManager,
) -> None:
    while True:
        print("\n--- Reservations ---")
        print("1. Create reservation")
        print("2. View reservation")
        print("3. Update reservation")
        print("4. Cancel reservation")
        print("5. List all reservations")
        print("6. Back")
        choice = input("Choose an option: ").strip()

        try:
            if choice == "6":
                return
            elif choice == "1":
                _create_reservation_prompt(reservations, tables, customers)
            elif choice == "2":
                _view_reservation_prompt(reservations)
            elif choice == "3":
                _update_reservation_prompt(reservations)
            elif choice == "4":
                _cancel_reservation_prompt(reservations)
            elif choice == "5":
                _list_reservations_prompt(reservations)
            else:
                print("Invalid choice.")
        except ValidationError as exc:
            print(f"Invalid input: {exc}")
        except NotImplementedError:
            print("That part isn't implemented yet (waiting on another module).")
        except ValueError:
            print("Please enter a whole number where one is expected.")


def _create_reservation_prompt(
    reservations: ReservationManager,
    tables: TableManager,
    customers: CustomerManager,
) -> None:
    customer_id = int(input("Customer ID: ").strip())
    if customers.view(customer_id) is None:
        print(f"No customer with ID {customer_id}.")
        return

    table_id = int(input("Table ID: ").strip())
    date = input("Date (YYYY-MM-DD): ").strip()
    time = input("Time (HH:MM): ").strip()
    party_size = int(input("Party size: ").strip())

    if tables.is_double_booked(table_id, date, time, reservations.list_all()):
        print(f"Table {table_id} is already booked at {date} {time}.")
        return

    reservation = reservations.create(customer_id, table_id, date, time, party_size)
    print(f"Created reservation #{reservation.id}.")


def _view_reservation_prompt(reservations: ReservationManager) -> None:
    reservation_id = int(input("Reservation ID: ").strip())
    reservation = reservations.view(reservation_id)
    print(reservation if reservation else "Not found.")


def _update_reservation_prompt(reservations: ReservationManager) -> None:
    reservation_id = int(input("Reservation ID: ").strip())
    field = input("Field to update (date/time/party_size/table_id): ").strip()
    raw_value = input("New value: ").strip()
    value = int(raw_value) if field in ("party_size", "table_id") else raw_value

    updated = reservations.update(reservation_id, **{field: value})
    print(updated if updated else "Not found.")


def _cancel_reservation_prompt(reservations: ReservationManager) -> None:
    reservation_id = int(input("Reservation ID: ").strip())
    print("Cancelled." if reservations.cancel(reservation_id) else "Not found.")


def _list_reservations_prompt(reservations: ReservationManager) -> None:
    all_reservations = reservations.list_all()
    if not all_reservations:
        print("No reservations yet.")
        return
    for reservation in all_reservations:
        print(reservation)


def table_menu(tables: TableManager, reservations: ReservationManager) -> None:
    # TODO(Member 3): display available tables, assign table prompts
    print("Table menu not implemented yet.")


def search_menu(reservations: ReservationManager) -> None:
    # TODO(Member 4): search/filter/report prompts
    print("Search & Reports menu not implemented yet.")


if __name__ == "__main__":
    run()
