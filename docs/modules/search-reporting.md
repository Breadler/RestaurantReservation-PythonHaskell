# Module: Search & Reporting

**Owner:** Member 4
**Status:** Not started

Covers Report.md sections 4.2/4.3 (Implementation), 5.2 (Test Cases), and the Search/Reporting-specific parts of 6.1 (Comparison). See [docs/design/project-structure.md](../design/project-structure.md) for the shared architecture and diagrams.

## Functionality Checklist
- [ ] View all reservations
- [ ] Search reservations
- [ ] Filter reservations
- [ ] Daily reservation summary (optional)
- [ ] Sorting (optional)

Files: `python/search.py` · `haskell/Search.hs`

---

## 1. Module Design
### Python (OOP)
[Describe how search/reporting operates over data exposed by `ReservationManager` — standalone functions vs. a service class.]

### Haskell (FP)
[Describe the pure functions in `Search.hs` that operate over `[Reservation]`, e.g. filters and folds.]

## 2. Implementation
### Python
[Explain `view_all()`, `search()`, `filter_by(...)`, and optional `daily_summary()`/`sort_by(...)`. Include key code extracts.]

### Haskell
[Explain `searchByDate`, `filterByStatus`, and optional `dailySummary`/`sortReservations`. Include key code extracts and type signatures.]

## 3. Code Explanation
[Walk through the filter/search criteria supported (by date, customer, table, status) and how they compose.]

## 4. Test Cases

| Test ID | Test Description | Input | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|
| SR-01 | View all reservations | | | | |
| SR-02 | Search by customer name | | | | |
| SR-03 | Filter by date | | | | |
| SR-04 | Filter by status (active/cancelled) | | | | |
| SR-05 | Daily reservation summary (optional) | | | | |
| SR-06 | Sort reservations by time (optional) | | | | |

## 5. Testing Results
[Summarize pass/fail outcomes once testing is complete.]

## 6. Challenges Encountered
[Note any difficulties, e.g. combining multiple filter criteria, keeping search in sync with the reservation module's data shape.]

## 7. Module-Specific Discussion (Python vs Haskell)
[Compare how each paradigm expressed search/filter — loops and list comprehensions vs. higher-order functions like `filter`/`map`.]
