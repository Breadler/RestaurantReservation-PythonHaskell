"""Test to demonstrate option 1 working with debug output."""

from table import TableManager
from reservation import ReservationManager

def _view_all_tables_prompt(tables: TableManager) -> None:
    """Display all tables."""
    print("\n=== All Tables ===", flush=True)
    print(f"{'ID':<5} {'Capacity':<10} {'Status':<20}", flush=True)
    print("-" * 35, flush=True)
    
    all_tables = tables.list_all()
    if not all_tables:
        print("No tables yet.", flush=True)
    else:
        for table in all_tables:
            print(f"{table.id:<5} {table.capacity:<10} {table.status:<20}", flush=True)
    
    print("", flush=True)  # Add blank line for readability

# Test simulation
print("=" * 50)
print("SIMULATING: Table Menu -> Press 1")
print("=" * 50)

tables = TableManager()
reservations = ReservationManager()

# Add some test tables
tables.add_table(4)
tables.add_table(6)
tables.add_table(8)

# Simulate the menu
print("\n--- Tables ---")
print("1. View all tables")
print("2. Check table availability")
print("3. Add new table")
print("4. Update table (capacity/status)")
print("5. Back")
choice = "1"  # Simulating user pressing 1
print(f"Choose an option: {choice}")
print(f"[DEBUG] You selected: '{choice}'", flush=True)

if choice == "1":
    print("[DEBUG] Executing option 1: View all tables", flush=True)
    _view_all_tables_prompt(tables)

print("\n" + "=" * 50)
print("✓ Test completed!")
print("=" * 50)
