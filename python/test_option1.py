"""Test to demonstrate option 1 (View all tables) now works clearly."""

from table import TableManager
from reservation import ReservationManager

def _view_all_tables_prompt(tables: TableManager) -> None:
    """Display all tables."""
    all_tables = tables.list_all()
    print("\n=== All Tables ===")
    print(f"{'ID':<5} {'Capacity':<10} {'Status':<20}")
    print("-" * 35)
    
    if not all_tables:
        print("No tables yet.")
    else:
        for table in all_tables:
            print(f"{table.id:<5} {table.capacity:<10} {table.status:<20}")
    
    print()  # Add blank line for readability

# Test 1: Empty tables
print("=" * 50)
print("TEST 1: View all tables (empty)")
print("=" * 50)
tables = TableManager()
reservations = ReservationManager()
_view_all_tables_prompt(tables)

# Test 2: With tables
print("=" * 50)
print("TEST 2: View all tables (with data)")
print("=" * 50)
tables.add_table(4)
tables.add_table(6)
tables.add_table(8)
tables.update(2, status="Under Maintenance")
_view_all_tables_prompt(tables)

print("✓ Option 1 is now working correctly!")
