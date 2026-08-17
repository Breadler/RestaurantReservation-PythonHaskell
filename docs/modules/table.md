# Module: Table Management

**Owner:** Member 3
**Status:** Done. Implemented and tested in both languages; code compiles/type-checks cleanly.

Covers Report.md sections 4.2/4.3 (Implementation), 5.2 (Test Cases), and the Table-specific parts of 6.1 (Comparison). See [docs/design/project-structure.md](../design/project-structure.md) for the shared architecture and diagrams, including the create-reservation/double-booking flowchart.

## Functionality Checklist
- [x] Display available tables
- [x] Prevent double booking (`is_double_booked` / `isDoubleBooked`)
- [x] Table management functions (add/list/update capacity & status)
- [x] Table status added beyond the original design: `Table` now carries `status`/`tableStatus` (`Active`/`Under Maintenance` in Python, `Ready`/`UnderMaintenance` in Haskell; the two languages picked different names for the same concept, worth a line in the report's comparison section)

**Integration note (found during review, now fixed):** "assign table to reservation" was never a separate function (by design, see [docs/design/project-structure.md](../design/project-structure.md)). It happens in the Reservation module's create flow. But that flow wasn't actually calling into this module's `is_double_booked`/`isDoubleBooked` (Haskell didn't call it at all; Python called it but never checked the table existed first). Both were fixed in `python/main.py`'s `_create_reservation_prompt` and `haskell/Main.hs`'s `createReservationPrompt` to check table-exists → table-status → double-booking, in that order, before creating a reservation. Re-verified working in both languages (nonexistent table rejected, double-booking rejected, valid booking succeeds).

Files: `python/table.py` · `haskell/Types.hs` (Table), `haskell/Table.hs`

---

## 1. Module Design
### Python (OOP)
`Table` is a `@dataclass` with `id`, `capacity`, and `status` (`"Active"` or `"Under Maintenance"`, defaulting to `"Active"`). `TableManager` wraps a `dict[int, Table]` keyed by ID plus a `_next_id` counter, and exposes `add_table`, `view`, `update`, `list_available`, `is_double_booked`, and `list_all`.

There is no stored "is this table booked" flag. Availability is computed on demand from the reservations list, so table state and reservation state can never drift out of sync.

### Haskell (FP)
`Table` is a record in `Types.hs` (`tableId`, `tableCapacity`, `tableStatus`), alongside a `TableStatus` type (`Ready` / `UnderMaintenance`). `Table.hs` has no manager and no stored state; it exposes two pure functions over `[Table]`/`[Reservation]`:
```haskell
listAvailable   :: String -> String -> [Table] -> [Reservation] -> [Table]
isDoubleBooked  :: Int -> String -> String -> [Reservation] -> Bool
```

## 2. Implementation
### Python
```python
def is_double_booked(self, table_id, date, time, reservations) -> bool:
    """Return True if the table already has an active reservation at
    the given date/time."""
    return any(
        reservation.status == "active"
        and reservation.table_id == table_id
        and reservation.date == date
        and reservation.time == time
        for reservation in reservations
    )

def list_available(self, date, time, reservations) -> List[Table]:
    """Return tables with no active reservation at the given date/time."""
    return [
        table for table in self.list_all()
        if table.status == "Active"
        and not self.is_double_booked(table.id, date, time, reservations)
    ]
```
`add_table()` creates and stores a new `Table` with status `"Active"`. `update()` accepts `capacity` and/or `status` keyword arguments and mutates the stored object.

### Haskell
```haskell
isDoubleBooked :: Int -> String -> String -> [Reservation] -> Bool
isDoubleBooked tableId date time reservations =
  any
    (\r -> reservationTableId r == tableId
      && reservationStatus r == Active
      && reservationDate r == date
      && reservationTime r == time)
    reservations

listAvailable :: String -> String -> [Table] -> [Reservation] -> [Table]
listAvailable date time tables reservations =
  filter
    (\tbl -> tableStatus tbl == Ready && not (isDoubleBooked (tableId tbl) date time reservations))
    tables
```

## 3. Code Explanation
`isDoubleBooked` is the core invariant: a table is booked at a given date/time if the reservation list contains an *active* reservation (cancelled ones don't count) for that exact table, date, and time. `listAvailable` builds on it directly, adding one more condition: the table's own status must be `Active`/`Ready`. There is no separate "assign table to reservation" function in either language; assigning a table is just creating a `Reservation` that carries a `table_id`, once `isDoubleBooked` and the table's status have both been checked by the caller. Keeping that as one step, rather than a create step plus a separate assign step, removes a class of bugs where the two could fall out of sync.

## 4. Test Cases

| Test ID | Test Description | Input | Expected Result | Status |
|---|---|---|---|---|
| TBL-01 | Add tables | capacities 4 and 2 | Two tables created with status Active/Ready | Pass (both) |
| TBL-02 | List all tables | N/A | Both tables returned | Pass (both) |
| TBL-03 | Detect an existing booking | table 1, date/time matching an active reservation | Returns true | Pass (both) |
| TBL-04 | Detect no booking on a different table | table 2, same date/time | Returns false | Pass (both) |
| TBL-05 | List available tables | date/time with table 1 booked | Only table 2 returned | Pass (both) |
| TBL-06 | Update table status | table 2 set to Under Maintenance/UnderMaintenance | Status updated | Pass (both) |
| TBL-07 | Availability excludes maintenance tables | table 2 under maintenance, different date/time | Only table 1 returned | Pass (both) |
| TBL-08 | View a nonexistent table | id=999 | Not-found response, no crash | Pass (Python; Haskell has no direct `viewTable` lookup, so this is exercised at the `Main.hs` CLI layer instead) |

Both languages were tested by calling `TableManager`/`Table.hs` directly with the same inputs, and produced identical results, for example `is_double_booked`/`isDoubleBooked` both returning `True` for table 1 and `False` for table 2 against the same reservation, and `list_available`/`listAvailable` both returning only the unbooked table.

## 5. Testing Results
All test cases pass in both Python and Haskell, with matching results for identical input.

## 6. Challenges Encountered
Deciding not to store a booking flag on `Table` itself, and instead always deriving availability from the reservations list, removed what would otherwise be the main source of bugs in this module (the flag and the reservations list disagreeing with each other).

## 7. Module-Specific Discussion (Python vs Haskell)
Python's `TableManager` holds tables in a dictionary and mutates a table's `status` in place via `setattr`-style attribute assignment inside `update()`. Haskell's `Table.hs` has no equivalent object: `listAvailable` and `isDoubleBooked` are ordinary pure functions over whatever `[Table]`/`[Reservation]` values are passed in, and updating a table's status (done in `Main.hs`) produces a new `Table` value with a record update (`t { tableStatus = UnderMaintenance }`) rather than mutating the original. The two languages also chose different names for the same status concept: `"Active"`/`"Under Maintenance"` strings in Python versus a dedicated `Ready`/`UnderMaintenance` algebraic type in Haskell, which the compiler checks exhaustively at every point the status is matched on, unlike Python's plain strings.
