#!/usr/bin/env python3
"""Standalone demo of the View All Tables feature."""

from table import TableManager

def main():
    print("=" * 50)
    print("TABLE MENU DEMO - View All Tables")
    print("=" * 50)
    
    tables = TableManager()
    
    # Add sample tables
    print("\nAdding sample tables...")
    t1 = tables.add_table(2)
    print(f"  Added: {t1}")
    t2 = tables.add_table(4)
    print(f"  Added: {t2}")
    t3 = tables.add_table(6)
    print(f"  Added: {t3}")
    t4 = tables.add_table(8)
    print(f"  Added: {t4}")
    
    # Update one table's status
    print("\nUpdating table 2's status to 'Under Maintenance'...")
    tables.update(2, status="Under Maintenance")
    
    # Display all tables
    print("\n" + "=" * 50)
    print("VIEW ALL TABLES SECTION:")
    print("=" * 50)
    
    all_tables = tables.list_all()
    if not all_tables:
        print("No tables yet.")
    else:
        print(f"\n{'ID':<5} {'Capacity':<10} {'Status':<20}")
        print("-" * 35)
        for table in all_tables:
            print(f"{table.id:<5} {table.capacity:<10} {table.status:<20}")
    
    print("\n" + "=" * 50)
    print("✓ Demo completed successfully!")
    print("=" * 50)

if __name__ == "__main__":
    main()
