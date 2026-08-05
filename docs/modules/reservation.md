# Module: Reservation Management

**Owner:** Member 1
**Status:** Done. Implemented and tested in both languages — Python via direct calls and the CLI; Haskell compiled with `ghc -Wall` (clean, no warnings) and run both as a built `.exe` (CLI flow) and via a standalone script exercising `Reservation.hs`/`Validation.hs` directly.

Covers Report.md sections 4.2/4.3 (Implementation), 5.2 (Test Cases), and the Reservation-specific parts of 6.1 (Comparison). See [docs/design/project-structure.md](../design/project-structure.md) for the shared architecture and diagrams.

## Functionality Checklist
- [x] Create reservation
- [x] View reservation
- [x] Update reservation
- [x] Cancel reservation
- [x] Reservation validation (date, time, party size) — linked customer/table checks live in the CLI layer (`main.py` / `Main.hs`), see Design notes below

Files: `python/reservation.py` · `haskell/Types.hs` (Reservation), `haskell/Reservation.hs`

---

## 1. Module Design
### Python (OOP)
`Reservation` is a `@dataclass` (id, customer_id, table_id, date, time, party_size, status). `ReservationManager` wraps a `dict[int, Reservation]` keyed by ID plus a `_next_id` counter, and exposes `create`/`view`/`update`/`cancel`/`list_all`. State lives *inside* the manager object and is mutated in place (`self._reservations[...] = ...`, `reservation.status = "cancelled"`).

Deliberate boundary: `ReservationManager` only validates its own fields (date/time/party_size via `validation.py`). It does **not** import `customer.py` or `table.py` — checking that the customer exists and the table is free happens in `main.py`'s `reservation_menu`, which already has access to all three managers. This keeps the module independently testable (see Test Cases below, all run without Customer/Table code existing).

### Haskell (FP)
`Reservation` is a record in `Types.hs` (shared with Members 2 and 3), plus `ReservationStatus = Active | Cancelled`. `Reservation.hs` has no manager object and no stored state at all — just four pure functions over `[Reservation]`:

```haskell
createReservation :: Reservation -> [Reservation] -> [Reservation]
viewReservation    :: Int -> [Reservation] -> Maybe Reservation
updateReservation  :: Int -> (Reservation -> Reservation) -> [Reservation] -> [Reservation]
cancelReservation  :: Int -> [Reservation] -> [Reservation]
```

Every one of them returns a *new* list rather than mutating the old one. The actual mutable state (the current list, and the next-ID counter) lives in an `IORef AppState` in `Main.hs` — i.e. Haskell forces the "this changes over time" part of the design to be an explicit, visible decision at the IO boundary, whereas Python lets it hide inside an object's `self`.

## 2. Implementation
### Python
`create()` validates then stores:
```python
def create(self, customer_id, table_id, date, time, party_size):
    date = validate_date(date)
    time = validate_time(time)
    party_size = validate_party_size(party_size)
    reservation = Reservation(id=self._next_id, customer_id=customer_id,
                               table_id=table_id, date=date, time=time,
                               party_size=party_size)
    self._reservations[reservation.id] = reservation
    self._next_id += 1
    return reservation
```
`update(reservation_id, **fields)` accepts arbitrary keyword fields, re-validates `date`/`time`/`party_size` if present, rejects unknown field names (raises `ValidationError`), then uses `setattr` to mutate the stored object directly. `cancel()` is a separate method that only flips `status` — kept distinct from `update()` so "edit details" and "cancel" stay separate operations, matching the system requirements list.

### Haskell
```haskell
createReservation reservation reservations = reservations ++ [reservation]

viewReservation rid = find ((== rid) . reservationId)

updateReservation rid f = map apply
  where apply r | reservationId r == rid = f r
                | otherwise               = r

cancelReservation rid = updateReservation rid (\r -> r { reservationStatus = Cancelled })
```
`updateReservation` takes a `Reservation -> Reservation` function rather than a field-name/value pair — the caller builds that function (e.g. `\r -> r { reservationDate = d }`) after validating, so `Reservation.hs` never has to know what "date" or "partysize" mean as strings. `cancelReservation` is just `updateReservation` applied to a specific update function, so cancel is a one-line reuse of update rather than separate logic — a direct consequence of updates being values (functions) instead of method calls.

## 3. Code Explanation
**ID generation:** Python keeps `_next_id` as manager state and increments it inside `create()`. Haskell can't do that (no mutable field inside a pure function), so the counter (`nextReservationId`) lives in `Main.hs`'s `AppState`, and the IO-level `createReservationPrompt` is responsible for reading it, using it, and incrementing it via `writeIORef`.

**Cancel representation:** cancellation is a status flag (`"cancelled"` / `Cancelled`), not a delete, in both languages — cancelled reservations stay visible in `list_all`/`listReservations` (needed for Member 4's search/reporting over "all reservations" including cancelled ones) and to prevent ID reuse.

**Validation purity (Haskell-specific):** `validateDate` takes `today :: Day` as an explicit argument instead of calling `getCurrentTime` itself, so the function stays pure and the actual clock read happens once, in `Main.hs`, right before it's needed. Python's `validate_date` just calls `date.today()` inline — no such split is needed since Python doesn't distinguish pure from effectful functions.

**Cross-module checks:** both `main.py`'s `reservation_menu` and `Main.hs`'s `reservationMenu` check for the customer via the Customer module (`customers.view(...)` / `viewCustomer`) before creating a reservation, and are *designed* to also check `tables.is_double_booked(...)` — Python's CLI already calls it; Haskell's does not yet (Member 3's `Table.hs` functions aren't implemented, so this is a follow-up once that module lands, mirroring the Python side).

**Handling other members' unfinished stubs:** calling into an unimplemented function raises `NotImplementedError` in Python and evaluates `error "TODO(Member N): ..."` in Haskell. Python's `run()` already wrapped submenu actions in `except NotImplementedError`. Haskell needed the equivalent — without it, hitting a stub (e.g. `Customer.viewCustomer` before Member 2 implements it) crashed the whole program with an uncaught `ErrorCall` instead of just failing that one action. Fixed by wrapping each reservation-menu action in `Main.hs` with a small `runAction` helper that catches `ErrorCall` and prints a message, mirroring Python's behavior exactly (confirmed by running both and comparing output — see Test Cases).

## 4. Test Cases

Python was run directly against `ReservationManager` and via the CLI's reservation submenu. Haskell was run two ways: directly against `Reservation.hs`/`Validation.hs` (a standalone script, equivalent to the Python direct calls) and via the built CLI executable (`ghc -O0 -o restaurant-reservation.exe Main.hs`).

| Test ID | Test Description | Input | Expected Result | Actual (Python) | Actual (Haskell) | Status |
|---|---|---|---|---|---|---|
| RES-01 | Create valid reservation | customer_id=1, table_id=2, date=2026-09-01, time=19:30, party_size=4 | Reservation created with id=1, status active | `Reservation(id=1, ..., status='active')` | `[Reservation {reservationId = 1, ..., reservationStatus = Active}]` | Pass (both) |
| RES-02 | View existing reservation | id=1 | Same record returned | Same record returned | `Just (Reservation {..., reservationStatus = Active})` | Pass (both) |
| RES-03 | Update reservation date/time | id=1, date=2026-09-02, time=20:00 | Record updated in place | `date='2026-09-02', time='20:00'` | `Just (Reservation {..., reservationDate = "2026-09-02", reservationTime = "20:00"})` | Pass (both) |
| RES-04 | Cancel reservation | id=1 | Status becomes cancelled | `status='cancelled'` | `Just (Reservation {..., reservationStatus = Cancelled})` | Pass (both) |
| RES-05 | Reject reservation with invalid (past) date | date=2020-01-01 | Rejected with a clear error | `ValidationError: Reservation date 2020-01-01 is in the past.` | `Left "Reservation date 2020-01-01 is in the past."` | Pass (both) |
| RES-05b | Reject reservation with malformed date | date="not-a-date" | Rejected with a clear error | `ValidationError: 'not-a-date' is not a valid date (expected YYYY-MM-DD).` | `Left "not-a-date is not a valid date (expected YYYY-MM-DD)."` | Pass (both) |
| RES-05c | Reject reservation with invalid party size | party_size=0 | Rejected with a clear error | `ValidationError: Party size must be at least 1.` | `Left "Party size must be at least 1."` | Pass (both) |
| RES-06 | Create with missing/unknown customer (via CLI) | customer_id=1, no customers exist yet | CLI reports the problem without crashing the submenu | `NotImplementedError` (Member 2's `CustomerManager.view` is a stub), caught, printed "That part isn't implemented yet (waiting on another module)." | `ErrorCall` (Member 2's `Customer.viewCustomer` is a stub), caught by `runAction`, printed "That part isn't implemented yet: TODO(Member 2): implement viewCustomer" | Pass (both) — correctly blocked on Member 2, neither crashes |
| RES-07 | View/cancel nonexistent reservation | id=999 | "Not found" / no-op, not a crash | `view` → `None`, `cancel` → `False` | `viewReservation 999 ...` → `Nothing`; `cancelReservation 999 ...` returns the list unchanged | Pass (both) |
| RES-08 | Update with unknown field | Python: `update(1, status="cancelled")` | Rejected — status must go through cancel, not update | `ValidationError: Unknown field(s): status` | Not separately exercised (Haskell's update takes a function, not a field name, at the `Reservation.hs` level; the CLI's field-name dispatch has an equivalent `_ -> Left ("Unknown field: " ++ field)` branch in `Main.hs`, same shape as the tested date/time/partysize branches, but not run this session) | Pass (Python); reviewed, not run (Haskell) |

## 5. Testing Results
All test cases pass in both languages, with one intentional exception either way: RES-06 is blocked on Member 2's customer lookup in both Python and Haskell — the point of that test is confirming the failure is caught cleanly and doesn't crash the app, which it does in both. RES-08's Haskell CLI path (unknown update field name) wasn't separately run — it can't be, until Member 2's work unblocks reservation creation through the CLI — but the underlying pattern is identical to the date/time/partysize branches that were tested.

## 6. Challenges Encountered
- Deciding where cross-module checks (customer exists, table free) belong: keeping them out of `ReservationManager`/`Reservation.hs` and in the CLI layer kept this module testable on its own, at the cost of the CLI layer needing to know about all three managers.
- Haskell's `validateDate` needing a passed-in "today" rather than reading the clock itself — a small thing, but it's the first place the pure/IO split became a real design decision rather than a slogan.
- First implementation of `Main.hs` looked up customers/reservations with local `find` calls instead of going through `Customer.hs`/`Reservation.hs`'s own lookup functions — worked, but silently bypassed the module boundary (and, as a side effect, let the create-flow "succeed" without ever touching Member 2's code). Fixed to call `viewCustomer`/`viewReservation` explicitly, which is what then surfaced the next issue below.
- That fix exposed a real bug once GHC was available to test with: an unimplemented stub (`error "TODO(Member 2): ..."`) crashed the entire Haskell program instead of just failing one menu action, unlike Python where `NotImplementedError` is caught centrally. Added a `runAction` handler in `Main.hs` (catches `ErrorCall` specifically, not all exceptions) so the two implementations behave the same way when they hit each other's unfinished stubs. This only turned up because the code was actually compiled and run — worth flagging for the other members too.

## 7. Module-Specific Discussion (Python vs Haskell)
The two implementations expose the *same* four operations but store state differently: Python's `ReservationManager` owns a dict and mutates it in place; Haskell has no equivalent object — `Reservation.hs`'s functions are all `[Reservation] -> ... -> [Reservation]`, and the single mutable cell (`IORef AppState`) lives at the very top of the program, in `Main.hs`. Practically, this means every Haskell function in this module can be tested by just calling it with a plain list and checking the list it returns — no setup/teardown of an object needed — while Python's tests need a fresh `ReservationManager()` per test to avoid state leaking between cases.

`cancelReservation`'s one-line reuse of `updateReservation` (`cancelReservation rid = updateReservation rid (\r -> r { reservationStatus = Cancelled })`) versus Python's separate `cancel()` method is a good concrete example for the report: in Haskell, "cancel" is just a specific *value* passed to the general update function; in Python it's a separate method because there's no lightweight way to pass "the change to make" as a value without also writing a small function object.

**"Not implemented yet" as a case study in error handling:** both languages needed the exact same safety net — catch a "this module isn't done" failure at the menu-action boundary so one missing piece doesn't take down the whole program — but reached it differently. Python's `NotImplementedError` is a normal class in its built-in exception hierarchy, so `except NotImplementedError` was a one-line, obvious addition. Haskell's `error "..."` isn't typed as a distinct "not implemented" error at all — it's the same generic `error` used for any partial function, caught as `ErrorCall` via `Control.Exception.catch`, which is a coarser net (it'd also catch someone else's careless `error` call meant as a genuine crash). This is a fair illustration of a real trade-off: Python's exceptions are cheap to reach for and specific by default; Haskell's `error`/`ErrorCall` mechanism is intentionally the "escape hatch of last resort" (idiomatic Haskell would model recoverable failure with `Either`/`Maybe`, as `Validation.hs` already does) — using it here for "TODO stub" was a scaffolding shortcut, not the idiomatic long-term answer.
