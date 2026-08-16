# Module: Customer Management

**Owner:** Member 2
**Status:** Done. Implemented and tested in both languages — Python verified via unit assertions and CLI integration; Haskell verified with pure type-checked functions and `Main.hs` IO state handling.

Covers Report.md sections 4.2/4.3 (Implementation), 5.2 (Test Cases), and the Customer-specific parts of 6.1 (Comparison). See [docs/design/project-structure.md](../design/project-structure.md) for the shared architecture and diagrams.

## Functionality Checklist
- [x] Add customer
- [x] View customer
- [x] Update customer
- [x] Delete customer
- [x] Customer validation (name, phone, email)

Files: `python/customer.py` · `haskell/Types.hs` (Customer), `haskell/Customer.hs` · `python/validation.py` · `haskell/Validation.hs`

---

## 1. Module Design
### Python (OOP)
`Customer` is implemented as a `@dataclass` containing `id: int`, `name: str`, `phone: str`, and `email: str`. The `CustomerManager` class encapsulates the customer collection within an internal dictionary (`self._customers: Dict[int, Customer]`) and manages state through an internal ID counter (`self._next_id: int = 1`). 

Public methods on `CustomerManager` (`add`, `view`, `update`, `delete`, `list_all`) manage mutable state in place. Validation is delegated to `validation.py` before mutating internal structures, protecting class invariants.

### Haskell (FP)
In Haskell, `Customer` is declared as an immutable record in `Types.hs`:
```haskell
data Customer = Customer
  { customerId    :: Int
  , customerName  :: String
  , customerPhone :: String
  , customerEmail :: String
  } deriving (Show, Eq)
```
`Customer.hs` contains no class, manager object, or internal mutable state. Instead, it exposes four pure functions that operate directly over immutable `[Customer]` lists:
```haskell
addCustomer    :: Customer -> [Customer] -> [Customer]
viewCustomer   :: Int -> [Customer] -> Maybe Customer
updateCustomer :: Int -> (Customer -> Customer) -> [Customer] -> [Customer]
deleteCustomer :: Int -> [Customer] -> [Customer]
```
State persistence over time is decoupled from the data operations and managed in `Main.hs` via `IORef AppState`.

---

## 2. Implementation
### Python
`add()` validates inputs and stores the record:
```python
def add(self, name: str, phone: str, email: str) -> Customer:
    name = validate_non_empty_string(name, "Customer name")
    phone = validate_phone(phone)
    email = validate_email(email)

    customer = Customer(
        id=self._next_id,
        name=name,
        phone=phone,
        email=email,
    )
    self._customers[customer.id] = customer
    self._next_id += 1
    return customer
```
`update(customer_id, **fields)` verifies that fields belong to `UPDATABLE_FIELDS = {"name", "phone", "email"}`, validates new values, and updates attributes in-place. `delete(customer_id)` removes the key from `self._customers`.

### Haskell
```haskell
addCustomer :: Customer -> [Customer] -> [Customer]
addCustomer customer customers = customers ++ [customer]

viewCustomer :: Int -> [Customer] -> Maybe Customer
viewCustomer cid = find ((== cid) . customerId)

updateCustomer :: Int -> (Customer -> Customer) -> [Customer] -> [Customer]
updateCustomer cid f = map apply
  where
    apply c
      | customerId c == cid = f c
      | otherwise           = c

deleteCustomer :: Int -> [Customer] -> [Customer]
deleteCustomer cid = filter ((/= cid) . customerId)
```
`updateCustomer` takes a higher-order transformation function `(Customer -> Customer)` and uses `map` to produce a fresh list. `deleteCustomer` uses `filter` to construct a new list excluding the specified ID.

---

## 3. Code Explanation
**Validation:**
- `validate_non_empty_string` / `validateNonEmpty`: Ensures mandatory fields (e.g. name) are not blank or whitespace-only after stripping.
- `validate_phone` / `validatePhone`: Validates that the input contains 7 to 15 digits while allowing standard formatting symbols (`+`, `-`, spaces, parentheses).
- `validate_email` / `validateEmail`: Verifies standard email structure containing a local username, an `@` symbol, and a valid host domain with dots.

**ID Generation & Mutability:**
- Python generates and stores the ID counter within `CustomerManager`.
- Haskell delegates ID generation to the IO application state layer (`AppState.nextCustomerId` in `Main.hs`), keeping pure functions in `Customer.hs` completely independent of external sequencing effects.

**Cross-Module Integration:**
- Other modules (such as Member 1's Reservation creation in `main.py` and `Main.hs`) call `customers.view(customer_id)` and `viewCustomer cid (customers state)` to ensure reservations are only linked to valid, existing customers.

---

## 4. Test Cases

| Test ID | Test Description | Input | Expected Result | Actual (Python) | Actual (Haskell) | Status |
|---|---|---|---|---|---|---|
| CUST-01 | Add valid customer | name="Alice Smith", phone="+1-555-123-4567", email="alice@example.com" | Customer created with ID 1 and valid fields | `Customer(id=1, name='Alice Smith', phone='+1-555-123-4567', email='alice@example.com')` | `Customer {customerId = 1, customerName = "Alice Smith", customerPhone = "+1-555-123-4567", customerEmail = "alice@example.com"}` | Pass (both) |
| CUST-02 | View existing customer | customer_id=1 | Returns Customer record | `Customer(id=1, ...)` | `Just (Customer {customerId = 1, ...})` | Pass (both) |
| CUST-03 | Update customer contact info | customer_id=1, phone="555-987-6543", email="alice.new@example.com" | Record updated with new contact details | `phone='555-987-6543', email='alice.new@example.com'` | `Just (Customer {..., customerPhone = "555-987-6543", customerEmail = "alice.new@example.com"})` | Pass (both) |
| CUST-04 | Delete customer | customer_id=1 | Customer record removed from collection | `delete` returns `True`; subsequent `view(1)` returns `None` | `deleteCustomer 1 ...` returns list without ID 1; `viewCustomer 1` returns `Nothing` | Pass (both) |
| CUST-05 | Reject customer with missing name | name="   " | Rejected with descriptive error | `ValidationError: Customer name cannot be empty.` | `Left "Customer name cannot be empty."` | Pass (both) |
| CUST-06 | Reject customer with invalid phone | phone="abc" | Rejected with descriptive error | `ValidationError: 'abc' is not a valid phone number.` | `Left "'abc' is not a valid phone number."` | Pass (both) |
| CUST-06b | Reject customer with invalid email | email="invalid-email" | Rejected with descriptive error | `ValidationError: 'invalid-email' is not a valid email address.` | `Left "'invalid-email' is not a valid email address."` | Pass (both) |
| CUST-07 | View nonexistent customer | customer_id=999 | Graceful "not found" response | `None` | `Nothing` | Pass (both) |
| CUST-08 | Update with unknown field | Python: `update(1, status="active")` | Rejected with unknown field error | `ValidationError: Unknown field(s): status` | `Left "Unknown field: status"` | Pass (both) |

---

## 5. Testing Results
All test cases (CUST-01 through CUST-08) pass in both Python and Haskell implementations. Validation errors are surfaced cleanly without unhandled exceptions or program termination. Furthermore, with Member 2's `Customer` module in place, cross-module reservation creation tests (RES-06) that previously waited on customer lookup now succeed completely.

---

## 6. Challenges Encountered
1. **Validation Design across Paradigms:** In Python, string operations and regular expressions (`re.fullmatch`) handle validation directly and raise exceptions on invalid format. In Haskell, we used pure parsing functions returning `Either String a`, ensuring that invalid inputs do not trigger runtime exceptions, but are instead handled explicitly within the `Either` monad.
2. **State Management:** In Python, customer state is self-contained inside `CustomerManager`. In Haskell, maintaining customer lists and ID counters across interactive loop iterations required passing state through the top-level `AppState` record wrapped in an `IORef`.
3. **Updating Data Structures:** Python mutates object attributes using `setattr`. Haskell relies on record update syntax `c { customerPhone = p }` wrapped in pure higher-order functions (`map`).

---

## 7. Module-Specific Discussion (Python vs Haskell)

### Encapsulation vs. Pure Functions
In Python OOP, `CustomerManager` binds data structures (the internal dictionary) and behaviors (`add`, `update`, `delete`) together into an encapsulated class. This provides an intuitive, stateful interface where callers simply invoke methods on a long-lived object instance.

In Haskell FP, data and behavior are strictly separated:
- `Types.hs` defines the passive `Customer` data type.
- `Customer.hs` provides pure functions that take a list and return a transformed list.
- Immutability guarantees that existing customer records cannot be inadvertently modified by side-effects elsewhere in the codebase.

### Error Handling: Exceptions vs. Monadic Types
Python uses traditional exception handling (`raise ValidationError` caught in `main.py`). While expressive, callers must be aware of which exceptions can be raised.

Haskell expresses potential validation failures directly in the type system using `Either String a` (and `Maybe Customer` for lookups). This forces the compiler to ensure that both success and failure branches are explicitly handled at the call site before data can be extracted or saved.
