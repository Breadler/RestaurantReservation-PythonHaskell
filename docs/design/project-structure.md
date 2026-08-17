# Project Structure & Diagrams

Shared design reference for Report.md sections 3.2 (Architecture / Module Structure), 3.3 (Data Structures Used), and 3.4 (Flowchart / Pseudocode / Class Diagram). Update this file as the design evolves; the final report text in [Report.md](../../Report.md) should summarize it and link back here.

## Repository Layout

Deliberately flat: plain scripts/modules, no packages, no build tooling beyond what each language needs at minimum. Python needs nothing but the interpreter; Haskell runs with `runghc` (no cabal/stack project). This keeps the code itself small so the group's effort goes into the paradigm comparison, not project plumbing.

```
RestaurantReservation-PythonHaskell/
├── Report.md
├── README.md
├── python/
│   ├── main.py           # entry point, menu-driven CLI
│   ├── customer.py       # Customer model + CustomerManager        (Member 2)
│   ├── reservation.py    # Reservation model + ReservationManager  (Member 1)
│   ├── table.py          # Table model + TableManager (availability, double-booking) (Member 3)
│   ├── search.py         # search / filter / reporting             (Member 4)
│   └── validation.py     # shared input validation
├── haskell/
│   ├── Main.hs            # entry point, IO loop / menu
│   ├── Types.hs           # Customer, Reservation, Table data types
│   ├── Customer.hs        # pure customer CRUD functions       (Member 2)
│   ├── Reservation.hs     # pure reservation CRUD functions    (Member 1)
│   ├── Table.hs           # availability, double-booking check (Member 3)
│   ├── Search.hs          # search / filter / reporting        (Member 4)
│   ├── Validation.hs      # shared input validation
│   └── SearchTest.hs      # standalone manual test harness for Search.hs (Member 4); run with `runghc SearchTest.hs`
└── docs/
    ├── design/                  # this file and other shared design notes
    └── modules/                 # one working file per member/module
```

Each same-named file pair (`python/reservation.py` <-> `haskell/Reservation.hs`) maps 1:1 to a report section and a group member's task, so the module split doubles as the writing assignment.

## Module Responsibility Map

| Module | Owner | Python | Haskell | Working doc |
|---|---|---|---|---|
| Reservation | Member 1 | `reservation.py` | `Types.hs` (Reservation), `Reservation.hs` | [modules/reservation.md](../modules/reservation.md) |
| Customer | Member 2 | `customer.py` | `Types.hs` (Customer), `Customer.hs` | [modules/customer.md](../modules/customer.md) |
| Table | Member 3 | `table.py` | `Types.hs` (Table), `Table.hs` | [modules/table.md](../modules/table.md) |
| Search & Reporting | Member 4 | `search.py` | `Search.hs` | [modules/search-reporting.md](../modules/search-reporting.md) |
| Validation | shared | `validation.py` | `Validation.hs` | n/a |
| Entry point | shared | `main.py` | `Main.hs` | n/a |

Note: there's no separate "assign table to reservation" function; assignment just *is* creating/updating a `Reservation` with a `table_id`, after `Table`'s availability check passes. Keeping that as one step (rather than a create step plus a separate assign step) removes a class of bugs where the two could get out of sync.

---

## Diagrams (Text Form)

### 1. High-Level Architecture

```mermaid
flowchart TD
    CLI["CLI / Menu<br/>(main.py, Main.hs)"]
    CustMgmt["Customer Management"]
    ResMgmt["Reservation Management"]
    TblMgmt["Table Management"]
    SearchRpt["Search & Reporting"]
    Validation["Validation (shared)"]
    Store[("Data Store (in-memory)")]

    CLI --> CustMgmt
    CLI --> ResMgmt
    CLI --> TblMgmt
    CLI --> SearchRpt

    CustMgmt --> Validation
    ResMgmt --> Validation
    TblMgmt --> Validation

    CustMgmt --> Store
    ResMgmt --> Store
    TblMgmt --> Store
    SearchRpt --> Store
```

### 2. Data Relationship (ER-style)

```mermaid
erDiagram
    CUSTOMER ||--o{ RESERVATION : makes
    TABLE ||--o{ RESERVATION : "is booked for"

    CUSTOMER {
        int id
        string name
        string phone
        string email
    }
    TABLE {
        int id
        int capacity
        string status
    }
    RESERVATION {
        int id
        int customer_id
        int table_id
        string date
        string time
        int party_size
        string status
    }
```
One customer -> many reservations. One reservation -> exactly one table. A table can only hold one active reservation per date/time slot (this constraint is what the double-booking check enforces).

**Note:** in the actual code, `Table`/`table.py` does **not** store an `is_booked` flag. Availability is computed on demand by `TableManager.list_available()`/`is_double_booked()` (Python) and `Table.listAvailable`/`isDoubleBooked` (Haskell) by scanning the reservations list for an active reservation on the same table/date/time. This avoids having two pieces of state (the flag and the reservations list) that could drift out of sync.

### 3. Python Class Diagram (OOP)

```mermaid
classDiagram
    class Customer {
        +int id
        +str name
        +str phone
        +str email
    }
    class CustomerManager {
        +add(name, phone, email) Customer
        +view(id) Customer
        +update(id, fields) Customer
        +delete(id) bool
        +list_all() List~Customer~
    }
    CustomerManager --> Customer : manages

    class Table {
        +int id
        +int capacity
        +str status
    }
    class TableManager {
        +add_table(capacity) Table
        +list_available(date, time, reservations) List~Table~
        +is_double_booked(table_id, date, time, reservations) bool
        +list_all() List~Table~
    }
    TableManager --> Table : manages

    class Reservation {
        +int id
        +int customer_id
        +int table_id
        +str date
        +str time
        +int party_size
        +str status
    }
    class ReservationManager {
        +create(customer_id, table_id, date, time, party_size) Reservation
        +view(id) Reservation
        +update(id, fields) Reservation
        +cancel(id) bool
        +list_all() List~Reservation~
    }
    ReservationManager --> Reservation : manages
```

### 4. Haskell Module/Type Diagram (FP)

```mermaid
flowchart TD
    Types["Types.hs<br/>Customer, Table, Reservation records"]
    CustomerHs["Customer.hs<br/>addCustomer, viewCustomer,<br/>updateCustomer, deleteCustomer"]
    ReservationHs["Reservation.hs<br/>createReservation, viewReservation,<br/>updateReservation, cancelReservation"]
    TableHs["Table.hs<br/>listAvailable, isDoubleBooked"]
    SearchHs["Search.hs<br/>searchByCustomer, filterByDate,<br/>filterByStatus, dailySummary, sortByTime"]
    ValidationHs["Validation.hs<br/>validateNonEmpty, validatePhone, validateEmail,<br/>validateDate, validateTime, validatePartySize"]
    MainHs["Main.hs<br/>entry point, menu loop, application state"]

    Types --> CustomerHs
    Types --> ReservationHs
    Types --> TableHs
    Types --> SearchHs

    CustomerHs --> MainHs
    ReservationHs --> MainHs
    TableHs --> MainHs
    SearchHs --> MainHs
    ValidationHs --> MainHs
```
Key contrast to note in the report: Python's managers hold mutable state (`self.reservations`); Haskell's functions are pure and return a new `[Reservation]` list rather than mutating one. State threading happens in `Main.hs` via `IORef`.

### 5. Main Menu Flowchart

```mermaid
flowchart TD
    Start([Start]) --> Menu["Show Main Menu:<br/>1 Customers · 2 Reservations<br/>3 Tables · 4 Search/Reports · 5 Exit"]
    Menu --> Choice{Choice}
    Choice -->|1| CustMenu[Customer submenu]
    Choice -->|2| ResMenu[Reservation submenu]
    Choice -->|3| TblMenu[Table submenu]
    Choice -->|4| SearchMenu[Search & Reports submenu]
    Choice -->|5| Exit([Exit])
    CustMenu --> Menu
    ResMenu --> Menu
    TblMenu --> Menu
    SearchMenu --> Menu
```

### 6. Create-Reservation Flow (validation + double-booking)

```mermaid
flowchart TD
    Start([Enter reservation details]) --> CustExists{Customer exists?}
    CustExists -->|No| Err1[Show error, return to menu]
    CustExists -->|Yes| TblExists{Table exists?}
    TblExists -->|No| Err2[Show error, return to menu]
    TblExists -->|Yes| TblMaint{Table under maintenance?}
    TblMaint -->|Yes| Err3[Show error, return to menu]
    TblMaint -->|No| DoubleBooked{Already booked at this date/time?}
    DoubleBooked -->|Yes| Err4[Show error, return to menu]
    DoubleBooked -->|No| Validate{Date, time, and party size valid?}
    Validate -->|No| Err5[Show error, return to menu]
    Validate -->|Yes| Create[Create reservation]
    Create --> Confirm([Confirm to user])
```
