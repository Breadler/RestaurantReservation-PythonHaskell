## 4.0 Implementation

### 4.1 Tools and Language Used

The Python implementation targets Python 3 and uses only the standard library (`dataclasses`, `typing`, `datetime`, `re`); no third-party packages are required. The Haskell implementation targets GHC and uses only `base` plus `time` (a library that ships with GHC itself), and is run directly with `runghc`, with no separate build tool or project file required. Both are plain console programs; no external services, databases, or GUI frameworks are used.

### 4.2 Implementation: Python

**Customer Management** (`customer.py`). `Customer` is a dataclass with `id`, `name`, `phone`, and `email`. `CustomerManager` stores customers in a dictionary keyed by ID and validates fields through `validation.py` before storing them:

```python
def add(self, name: str, phone: str, email: str) -> Customer:
    """Create and store a new customer after validating fields."""
    name = validate_non_empty_string(name, "Customer name")
    phone = validate_phone(phone)
    email = validate_email(email)

    customer = Customer(id=self._next_id, name=name, phone=phone, email=email)
    self._customers[customer.id] = customer
    self._next_id += 1
    return customer
```

`update()` accepts keyword fields, rejects unknown field names, re-validates any field being changed, and updates the stored object's attributes with `setattr`. `delete()` and `view()` operate directly on the dictionary; `list_all()` returns its values.

**Reservation Management** (`reservation.py`). `Reservation` is a dataclass with `id`, `customer_id`, `table_id`, `date`, `time`, `party_size`, and `status` (defaulting to `"active"`). `ReservationManager` validates its own fields (date, time, party size) and stores the record; it does not check that the referenced customer or table exist; that check is made by the caller before `create()` is invoked, which keeps this module independent of the customer and table modules:

```python
def create(self, customer_id, table_id, date, time, party_size) -> Reservation:
    """Validate fields and create a new reservation."""
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

`cancel()` sets `status` to `"cancelled"` rather than removing the record, so cancelled reservations remain visible to search and reporting. `update()` is kept separate from `cancel()` so that editing a reservation's details and cancelling it remain distinct operations.

**Table Management** (`table.py`). `Table` is a dataclass with `id`, `capacity`, and `status` (`"Active"` or `"Under Maintenance"`, defaulting to `"Active"`). `TableManager` provides `add_table()`, `view()`, `update()`, `list_all()`, and the two functions that enforce the double-booking invariant:

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

**Search & Reporting** (`search.py`). A set of standalone functions that filter or summarise a list of reservations already produced by the reservation module; they never create, update, or cancel a reservation themselves:

```python
def filter_by_status(reservations, status):
    return [r for r in reservations if r.status.lower() == status.lower()]

def daily_summary(reservations, date):
    daily_reservations = filter_by_date(reservations, date)
    return {
        "date": date,
        "total_reservations": len(daily_reservations),
        "total_guests": sum(r.party_size for r in daily_reservations),
    }
```

**Validation** (`validation.py`). Shared functions used by all three managers, each raising `ValidationError` (a subclass of `ValueError`) with a descriptive message on invalid input, and returning the cleaned value otherwise. For example, `validate_phone` strips the input, checks it only contains digits and common formatting characters, and checks the digit count is between 7 and 15.

**Entry Point** (`main.py`). A single `run()` function drives the top-level menu and dispatches to a submenu for Customers, Reservations, Tables, or Search & Reports. Each submenu loops on its own until the user chooses "Back", catching `ValidationError` and `ValueError` from its actions so a single bad entry does not exit the submenu.

### 4.3 Implementation: Haskell

**Types** (`Types.hs`). `Customer`, `Table`, and `Reservation` are declared as immutable records, alongside two small enumerations, `TableStatus` (`Ready` / `UnderMaintenance`) and `ReservationStatus` (`Active` / `Cancelled`):

```haskell
data Reservation = Reservation
  { reservationId         :: Int
  , reservationCustomerId :: Int
  , reservationTableId    :: Int
  , reservationDate       :: String
  , reservationTime       :: String
  , partySize             :: Int
  , reservationStatus     :: ReservationStatus
  } deriving (Show, Eq)
```

**Customer Management** (`Customer.hs`). Four pure functions over `[Customer]`, each returning a new list rather than mutating one:

```haskell
addCustomer :: Customer -> [Customer] -> [Customer]
addCustomer customer customers = customers ++ [customer]

updateCustomer :: Int -> (Customer -> Customer) -> [Customer] -> [Customer]
updateCustomer cid f = map apply
  where apply c | customerId c == cid = f c
                | otherwise           = c

deleteCustomer :: Int -> [Customer] -> [Customer]
deleteCustomer cid = filter ((/= cid) . customerId)
```

`updateCustomer` takes the change to make as a function (`Customer -> Customer`) rather than a field name and value, so the caller decides what "update" means for a given call by supplying the appropriate function.

**Reservation Management** (`Reservation.hs`). The same shape as `Customer.hs`. Notably, `cancelReservation` is implemented as `updateReservation` applied to one specific update function, rather than as separate logic:

```haskell
cancelReservation :: Int -> [Reservation] -> [Reservation]
cancelReservation rid = updateReservation rid (\r -> r { reservationStatus = Cancelled })
```

**Table Management** (`Table.hs`). `isDoubleBooked` and `listAvailable` mirror their Python counterparts as pure functions over `[Table]` and `[Reservation]`:

```haskell
listAvailable :: String -> String -> [Table] -> [Reservation] -> [Table]
listAvailable date time tables reservations =
  filter
    (\tbl -> tableStatus tbl == Ready
             && not (isDoubleBooked (tableId tbl) date time reservations))
    tables
```

**Search & Reporting** (`Search.hs`). Higher-order functions (`filter`, `map`, `sum`, `sortOn`) replace Python's list comprehensions and built-ins:

```haskell
dailySummary :: String -> [Reservation] -> (Int, Int)
dailySummary date reservations =
  let dailyReservations = filterByDate date reservations
  in (length dailyReservations, sum (map partySize dailyReservations))
```

**Validation** (`Validation.hs`). Each validator returns `Either String a`: `Left` with an error message, or `Right` with the validated value. `validateDate` takes the current date as an explicit argument (rather than reading the system clock itself), so the function itself stays pure; the one place in the program that actually reads the clock is `Main.hs`:

```haskell
validateDate :: Day -> String -> Either String String
validateDate today value =
  case parseTimeM True defaultTimeLocale "%Y-%m-%d" value of
    Nothing -> Left (value ++ " is not a valid date (expected YYYY-MM-DD).")
    Just d
      | d < today -> Left ("Reservation date " ++ value ++ " is in the past.")
      | otherwise -> Right value
```

**Entry Point** (`Main.hs`). A single `IORef` holds the whole application state (customers, reservations, tables, and the next-ID counters for customers and reservations). The top-level menu loop reads and writes this reference between prompts; each submenu (Customers, Reservations, Tables, Search & Reports) is its own recursive `IO` action that loops until "Back" is chosen. Building a valid `Reservation` from raw input is expressed as a small `Either`-based computation that short-circuits on the first invalid field:

```haskell
buildReservation :: Day -> Int -> Int -> Int -> String -> String -> Int -> Either String Reservation
buildReservation today rid custId tblId dateStr timeStr size = do
  date'  <- validateDate today dateStr
  time'  <- validateTime timeStr
  size'  <- validatePartySize size
  Right Reservation { reservationId = rid, reservationCustomerId = custId
                     , reservationTableId = tblId, reservationDate = date'
                     , reservationTime = time', partySize = size'
                     , reservationStatus = Active }
```

### 4.4 Key Language Concepts Applied

Both implementations apply: primitive and structured data types, functions and methods, conditional and iterative control structures, modular file organisation, variable scope, and input validation. The Python implementation additionally demonstrates encapsulation (state and behaviour bound together in manager classes) and default/keyword arguments. The Haskell implementation additionally demonstrates immutability, pure functions, algebraic data types, pattern matching, higher-order functions, and explicit handling of effectful computation through `IO` and `Either`.

### 4.5 Code Organization

Each language's source is a flat set of single-purpose files (one per functional area, plus a shared validation module and an entry point) with no nested packages or subfolders. The two file sets mirror each other one-to-one (`customer.py` / `Customer.hs`, `reservation.py` / `Reservation.hs`, `table.py` / `Table.hs`, `search.py` / `Search.hs`, `validation.py` / `Validation.hs`, `main.py` / `Main.hs`), which keeps the two implementations straightforward to compare file-by-file.

### 4.6 Sample Output

**Figure 4.1: Main menu**

```
=== Restaurant Reservation System ===
1. Customers
2. Reservations
3. Tables
4. Search & Reports
5. Exit
Choose an option:
```

**Figure 4.2: Successful reservation creation (Python)**

```
--- Reservations ---
1. Create reservation
2. View reservation
3. Update reservation
4. Cancel reservation
5. List all reservations
6. Back
Choose an option: Customer ID: Table ID: Date (YYYY-MM-DD): Time (HH:MM): Party size: Created reservation #1.
```

**Figure 4.3: Successful reservation creation (Haskell)**

```
--- Reservations ---
1. Create reservation
2. View reservation
3. Update reservation
4. Cancel reservation
5. List all reservations
6. Back
Choose an option: Customer ID: Table ID: Date (YYYY-MM-DD): Time (HH:MM): Party size: Created reservation #1.
```

The two implementations produce equivalent output for the same sequence of inputs, despite the underlying code representing and updating state in different ways.
