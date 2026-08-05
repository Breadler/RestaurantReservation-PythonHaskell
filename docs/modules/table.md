# Module: Table Management

**Owner:** Member 3
**Status:** Not started

Covers Report.md sections 4.2/4.3 (Implementation), 5.2 (Test Cases), and the Table-specific parts of 6.1 (Comparison). See [docs/design/project-structure.md](../design/project-structure.md) for the shared architecture and diagrams, including the create-reservation/double-booking flowchart.

## Functionality Checklist
- [ ] Display available tables
- [ ] Assign tables to reservations
- [ ] Prevent double booking
- [ ] Table management functions (add/list/status)

Files: `python/table.py` · `haskell/Types.hs` (Table), `haskell/Table.hs`

---

## 1. Module Design
### Python (OOP)
[Describe the `Table` class and `TableManager` class: attributes, methods, how availability/booking state is stored.]

### Haskell (FP)
[Describe the `Table` data type and the pure functions in `Table.hs`: signatures, how availability checks and assignment return new values instead of mutating.]

## 2. Implementation
### Python
[Explain `list_available()`, `assign()`, `is_double_booked()` on `TableManager`. Include key code extracts.]

### Haskell
[Explain `listAvailable`, `assignTable`, `isDoubleBooked`. Include key code extracts and type signatures.]

## 3. Code Explanation
[Walk through the double-booking check logic in detail — this is the module's core algorithm and should be explained precisely for both languages.]

## 4. Test Cases

| Test ID | Test Description | Input | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|
| TBL-01 | Display available tables | | | | |
| TBL-02 | Assign table to reservation | | | | |
| TBL-03 | Reject assignment to already-booked table/time | | | | |
| TBL-04 | Free table after reservation cancelled | | | | |
| TBL-05 | Reject assignment when party size exceeds capacity | | | | |

## 5. Testing Results
[Summarize pass/fail outcomes once testing is complete.]

## 6. Challenges Encountered
[Note any difficulties, e.g. modeling time-slot overlap, keeping table state consistent across cancels/reassignments.]

## 7. Module-Specific Discussion (Python vs Haskell)
[Compare how each paradigm handled the double-booking invariant — mutable checks vs. pure functions over immutable lists.]
