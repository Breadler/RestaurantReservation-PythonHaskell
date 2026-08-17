## 5.0 Testing and Results

### 5.1 Testing Strategy

Each module was tested directly (calling its functions with representative data) and through the console menu, in both languages, using the same inputs so results could be compared side by side. Testing covered normal input, invalid input, boundary cases (a nonexistent ID, an empty collection), and the cross-module checks used when creating a reservation.

### 5.2 Test Cases

**Table 5.1: Customer Management**

| Test ID | Description | Input | Expected Result | Status |
|---|---|---|---|---|
| CUST-01 | Add valid customer | name="Alice Smith", phone="+1-555-123-4567", email="alice@example.com" | Customer created with ID 1 | Pass |
| CUST-02 | View existing customer | id=1 | Returns the stored record | Pass |
| CUST-03 | Update customer contact info | id=1, phone="555-987-6543", email="alice.new@example.com" | Record updated | Pass |
| CUST-04 | Delete customer | id=1 | Record removed; subsequent view returns not-found | Pass |
| CUST-05 | Reject customer with missing name | name="   " | Rejected: "Name cannot be empty." | Pass |
| CUST-06 | Reject customer with invalid phone | phone="abc" | Rejected: "not a valid phone number." | Pass |
| CUST-07 | Reject customer with invalid email | email="invalid-email" | Rejected: "not a valid email address." | Pass |
| CUST-08 | View nonexistent customer | id=999 | Not-found response, no crash | Pass |
| CUST-09 | Update with unknown field | field="status" | Rejected: unknown field error | Pass |

**Table 5.2: Reservation Management**

| Test ID | Description | Input | Expected Result | Status |
|---|---|---|---|---|
| RES-01 | Create valid reservation | customer_id=1, table_id=2, date=2026-09-01, time=19:30, party_size=4 | Reservation created, status active | Pass |
| RES-02 | View existing reservation | id=1 | Returns the stored record | Pass |
| RES-03 | Update reservation date/time | id=1, date=2026-09-02, time=20:00 | Record updated in place | Pass |
| RES-04 | Cancel reservation | id=1 | Status becomes cancelled; record still listed | Pass |
| RES-05 | Reject reservation with a past date | date=2020-01-01 | Rejected: "is in the past." | Pass |
| RES-06 | Reject reservation with a malformed date | date="not-a-date" | Rejected: "not a valid date" | Pass |
| RES-07 | Reject reservation with invalid party size | party_size=0 | Rejected: "must be at least 1." | Pass |
| RES-08 | Create against a nonexistent table | table_id=999 (never added) | Rejected: "No table with ID 999." | Pass |
| RES-09 | Create against a table under maintenance | table with status Under Maintenance | Rejected: "is under maintenance." | Pass |
| RES-10 | Create a double-booking | same table, date, and time as an existing active reservation | Rejected: "already booked at ..." | Pass |
| RES-11 | View/cancel a nonexistent reservation | id=999 | Not-found response, no crash | Pass |
| RES-12 | Update with an unknown field | field="status" | Rejected: unknown field error | Pass |

**Table 5.3: Table Management**

| Test ID | Description | Input | Expected Result | Status |
|---|---|---|---|---|
| TBL-01 | Add tables | capacities 4 and 2 | Two tables created with status Active | Pass |
| TBL-02 | List all tables | N/A | Both tables returned | Pass |
| TBL-03 | Detect an existing booking | table 1, date/time matching an active reservation | Returns true | Pass |
| TBL-04 | Detect no booking on a different table | table 2, same date/time | Returns false | Pass |
| TBL-05 | List available tables | date/time with table 1 booked | Only table 2 returned | Pass |
| TBL-06 | Update table status | table 2 set to Under Maintenance | Status updated | Pass |
| TBL-07 | Availability excludes maintenance tables | table 2 under maintenance, different date/time | Only table 1 returned | Pass |
| TBL-08 | View a nonexistent table | id=999 | Not-found response, no crash | Pass |

**Table 5.4: Search & Reporting**

Using a fixed set of four reservations (two customers with two reservations each, spread across two dates, one cancelled):

| Test ID | Description | Input | Expected Result | Status |
|---|---|---|---|---|
| SR-01 | View all reservations | N/A | All 4 reservations returned | Pass |
| SR-02 | Search by customer | customer_id=1 | The 2 reservations for that customer | Pass |
| SR-03 | Filter by date | date="2026-08-20" | The 3 reservations on that date | Pass |
| SR-04 | Filter by status | status="cancelled" | The 1 cancelled reservation | Pass |
| SR-05 | Daily summary | date="2026-08-20" | 3 reservations, 11 total guests | Pass |
| SR-06 | Sort by date and time | N/A | Reservations returned in chronological order | Pass |

### 5.3 Error and Edge Cases

The system was tested against empty input, malformed numbers and dates, references to records that do not exist, and attempts to book an unavailable table. In every case tested, the program reports a clear message and returns to the relevant menu rather than stopping or producing an incorrect result. Menu navigation itself was also tested with invalid menu choices, which are rejected with an "Invalid choice." message and re-prompted.

### 5.4 Testing Evidence

**Figure 5.1: Rejecting a reservation against a nonexistent table (Python)**
```
Choose an option: Customer ID: Table ID: No table with ID 999.
```

**Figure 5.2: Rejecting a double-booked reservation (Haskell)**
```
Choose an option: Customer ID: Table ID: Date (YYYY-MM-DD): Time (HH:MM): Party size: Table 1 is already booked at 2026-09-01 19:00.
```

**Figure 5.3: Daily summary output (identical result in both languages)**
```
Date: 2026-08-20
Total reservations: 3
Total guests: 11
```

### 5.5 Results Summary

All test cases listed above pass in both the Python and the Haskell implementation, using the same inputs and producing equivalent results. Invalid input is consistently rejected with a descriptive message rather than causing a crash, and the double-booking invariant holds in both languages.
