"""Test script to simulate accessing the table menu from main."""

from table import TableManager
from reservation import ReservationManager
from customer import CustomerManager

def _view_all_tables_prompt(tables: TableManager) -> None:
    """Display all tables."""
    all_tables = tables.list_all()
    if not all_tables:
        print("No tables yet.")
        return
    print("\nAll Tables:")
    print(f"{'ID':<5} {'Capacity':<10} {'Status':<20}")
    print("-" * 35)
    for table in all_tables:
        print(f"{table.id:<5} {table.capacity:<10} {table.status:<20}")

def table_menu(tables: TableManager, reservations: ReservationManager) -> None:
    """Table management submenu: view/add/update tables, check availability."""
    while True:
        print("\n--- Tables ---")
        print("1. View all tables")
        print("2. Check table availability")
        print("3. Add new table")
        print("4. Update table (capacity/status)")
        print("5. Back")
        choice = input("Choose an option: ").strip()

        try:
            if choice == "5":
                return
            elif choice == "1":
                _view_all_tables_prompt(tables)
            elif choice == "2":
                print("Not implemented yet")
            elif choice == "3":
                print("Not implemented yet")
            elif choice == "4":
                print("Not implemented yet")
            else:
                print("Invalid choice.")
        except Exception as e:
            print(f"Error: {e}")

# Test with actual data
print("=== Testing Table Menu ===\n")
tables = TableManager()
reservations = ReservationManager()

# Pre-populate with some tables
tables.add_table(4)
tables.add_table(6)
tables.add_table(8)

# Simulate the menu
print("Simulating: Main menu -> Option 3 (Tables)\n")
table_menu(tables, reservations)
print("\nTable menu test completed!")
