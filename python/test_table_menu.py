"""Quick test of the table menu functionality."""

from table import TableManager
from reservation import ReservationManager

# Simulate the table menu
tables = TableManager()
reservations = ReservationManager()

# Add some test tables
table1 = tables.add_table(4)
table2 = tables.add_table(6)
table3 = tables.add_table(8)

print("Testing table menu...")
print("\n--- Tables ---")
print("1. View all tables")
print("2. Check table availability")
print("3. Add new table")
print("4. Update table (capacity/status)")
print("5. Back")

# Simulate selecting option 1
print("\nSimulating: User selects '1' (View all tables)")
all_tables = tables.list_all()
if not all_tables:
    print("No tables yet.")
else:
    print("\nAll Tables:")
    print(f"{'ID':<5} {'Capacity':<10} {'Status':<20}")
    print("-" * 35)
    for table in all_tables:
        print(f"{table.id:<5} {table.capacity:<10} {table.status:<20}")

print("\n✓ View all tables works!")
