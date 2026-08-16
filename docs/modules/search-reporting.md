# Module: Search & Reporting

**Owner:** Member 4
**Status:** Completed

Covers Report.md sections 4.2/4.3 (Implementation), 5.2 (Test Cases), and the Search/Reporting-specific parts of 6.1 (Comparison). See [docs/design/project-structure.md](../design/project-structure.md) for the shared architecture and diagrams.

## Functionality Checklist

* [x] View all reservations
* [x] Search reservations by customer ID
* [x] Filter reservations by date
* [x] Filter reservations by status
* [x] Daily reservation summary
* [x] Sort reservations by date and time

Files: `python/search.py` · `haskell/Search.hs`

---

## 1. Module Design

### Python (OOP)

The Python Search and Reporting module works with the `Reservation` objects created and managed by the reservation management module. The search functions do not create, update, or cancel reservations. Instead, they receive a list of existing reservations and return the matching results.

The module is implemented using standalone functions in `search.py`. These functions operate on reservation objects and access attributes such as `customer_id`, `date`, `time`, `party_size`, and `status`.

The Search & Reports menu in `main.py` connects these functions to the console interface. This allows the user to view all reservations, search for a customer's reservations, filter records, generate a daily summary, and sort reservations.

### Haskell (FP)

The Haskell Search and Reporting module follows the functional programming paradigm. Reservation information is represented using `Reservation` records, while collections of reservations are stored as `[Reservation]`.

Functions in `Search.hs` are pure functions. They receive reservation data as input and return new results without changing the original reservation list.

Higher-order functions such as `filter` and `map` are used together with functions such as `sum`, `length`, and `sortOn`. This allows the same search and reporting requirements to be implemented using functional data transformations.

---

## 2. Implementation

### Python

The Python version contains the following functions:

#### `search_by_customer()`

Searches for reservations belonging to a specific customer ID.

```python
def search_by_customer(reservations, customer_id):
    return [
        reservation
        for reservation in reservations
        if reservation.customer_id == customer_id
    ]
```

#### `filter_by_date()`

Returns reservations that match a selected date.

```python
def filter_by_date(reservations, date):
    return [
        reservation
        for reservation in reservations
        if reservation.date == date
    ]
```

#### `filter_by_status()`

Returns reservations according to their status, such as active or cancelled.

```python
def filter_by_status(reservations, status):
    return [
        reservation
        for reservation in reservations
        if reservation.status.lower() == status.lower()
    ]
```

#### `daily_summary()`

Generates a summary for a selected date by calculating the total number of reservations and the total number of guests.

```python
def daily_summary(reservations, date):
    daily_reservations = filter_by_date(reservations, date)

    return {
        "date": date,
        "total_reservations": len(daily_reservations),
        "total_guests": sum(
            reservation.party_size
            for reservation in daily_reservations
        )
    }
```

#### `sort_by_time()`

Sorts reservations according to their date and time.

```python
def sort_by_time(reservations):
    return sorted(
        reservations,
        key=lambda reservation: (
            reservation.date,
            reservation.time
        )
    )
```

The functions are connected to the Search & Reports menu in `main.py`, allowing the user to access all functions through the console interface.

### Haskell

The Haskell implementation provides the same main functions:

* `searchByCustomer`
* `filterByDate`
* `filterByStatus`
* `dailySummary`
* `sortByTime`

#### `searchByCustomer`

```haskell
searchByCustomer :: Int -> [Reservation] -> [Reservation]
searchByCustomer customerId reservations =
    filter
        (\reservation ->
            reservationCustomerId reservation == customerId
        )
        reservations
```

The `filter` function keeps only reservations where the customer ID matches the requested ID.

#### `filterByDate`

```haskell
filterByDate :: String -> [Reservation] -> [Reservation]
filterByDate date reservations =
    filter
        (\reservation ->
            reservationDate reservation == date
        )
        reservations
```

This function returns only reservations that match the selected date.

#### `filterByStatus`

```haskell
filterByStatus :: ReservationStatus -> [Reservation] -> [Reservation]
filterByStatus status reservations =
    filter
        (\reservation ->
            reservationStatus reservation == status
        )
        reservations
```

Instead of using ordinary strings, the Haskell version uses the `ReservationStatus` data type with values such as `Active` and `Cancelled`.

#### `dailySummary`

```haskell
dailySummary :: String -> [Reservation] -> (Int, Int)
dailySummary date reservations =
    let dailyReservations = filterByDate date reservations
        totalReservations = length dailyReservations
        totalGuests = sum (map partySize dailyReservations)
    in
        (totalReservations, totalGuests)
```

The function first filters reservations by date. It then counts the reservations using `length` and calculates the total number of guests using `map` and `sum`.

#### `sortByTime`

```haskell
sortByTime :: [Reservation] -> [Reservation]
sortByTime reservations =
    sortOn
        (\reservation ->
            (reservationDate reservation, reservationTime reservation)
        )
        reservations
```

The reservations are sorted by date first and then by time.

---

## 3. Code Explanation

### Search by Customer

The customer search function allows the user to enter a customer ID and retrieve all reservations associated with that customer.

In Python, a list comprehension checks the `customer_id` attribute of each reservation object.

In Haskell, the higher-order function `filter` checks the `reservationCustomerId` field of each reservation record.

Both implementations therefore produce the same result using different programming styles.

### Filter by Date

The date filter returns reservations that match a selected date.

Python compares the `date` attribute of each reservation object with the requested date.

Haskell performs the same comparison using `filter` and the `reservationDate` record field.

### Filter by Status

The status filter allows active and cancelled reservations to be displayed separately.

The Python version stores the status as a string and uses lowercase conversion so that differences in capitalisation do not affect the result.

The Haskell version uses the `ReservationStatus` data type. This allows values such as `Active` and `Cancelled` to be compared directly.

### Daily Reservation Summary

The daily summary provides:

1. Total number of reservations for the selected date.
2. Total number of guests for the selected date.

The Python implementation uses `len()` and `sum()` after filtering the reservation list.

The Haskell implementation uses `length`, `map`, and `sum`.

During testing, the selected date `2026-08-20` contained three reservations with party sizes of 2, 4, and 5. Therefore, the expected summary was three reservations and eleven guests.

### Sorting

The sorting feature arranges reservations according to date and time.

Python uses the built-in `sorted()` function with date and time as the sorting key.

Haskell uses `sortOn` with the `reservationDate` and `reservationTime` fields.

Both implementations produce reservations in chronological order.

---

## 4. Test Cases

The Search and Reporting module was tested using four sample reservations.

| Test ID | Test Description               | Input                 | Expected Result                         | Actual Result                                   | Status |
| ------- | ------------------------------ | --------------------- | --------------------------------------- | ----------------------------------------------- | ------ |
| SR-01   | View all reservations          | 4 sample reservations | All 4 reservations are displayed        | All 4 reservations were displayed correctly     | Pass   |
| SR-02   | Search by customer ID          | Customer ID = 1       | Reservations #1 and #3 are returned     | Reservations #1 and #3 were returned            | Pass   |
| SR-03   | Filter by date                 | 2026-08-20            | Reservations #1, #2 and #4 are returned | Reservations #1, #2 and #4 were returned        | Pass   |
| SR-04   | Filter by status               | Cancelled             | Only Reservation #3 is returned         | Reservation #3 was returned                     | Pass   |
| SR-05   | Daily reservation summary      | 2026-08-20            | 3 reservations and 11 total guests      | Result returned `(3, 11)`                       | Pass   |
| SR-06   | Sort reservations by date/time | 4 sample reservations | Order: #2, #1, #4, #3                   | Reservations were returned in the correct order | Pass   |

---

## 5. Testing Results

All six Search and Reporting test cases were completed successfully.

The Python and Haskell implementations were able to perform reservation viewing, customer-based searching, date filtering, status filtering, daily reservation summaries, and date/time sorting.

The real-data Haskell test used four sample reservations and produced the expected output for all six test cases. The daily summary for `2026-08-20` correctly returned three reservations and eleven guests.

No functional errors were identified in the Search and Reporting module during final testing. Therefore, SR-01 to SR-06 achieved a Pass result.

---

## 6. Challenges Encountered

One challenge was ensuring that the Python and Haskell implementations provided the same behaviour while using different programming paradigms.

The Python version operates on `Reservation` objects and accesses their attributes directly. In comparison, the Haskell version operates on immutable `Reservation` records and uses pure functions to transform reservation lists.

Another challenge was keeping the Search and Reporting module compatible with the data structures created by the Reservation module. The search functions had to use the same customer IDs, dates, times, statuses, and party-size fields as the existing reservation implementation.

The status implementation was also slightly different between the two languages. Python uses strings such as `"active"` and `"cancelled"`, whereas Haskell uses the `ReservationStatus` data type with the constructors `Active` and `Cancelled`.

Testing with multiple reservations was therefore important to confirm that both implementations returned the correct records and summary values.

---

## 7. Module-Specific Discussion: Python vs Haskell

Although the Python and Haskell implementations provide the same Search and Reporting functionality, they express the solution differently because they use different programming paradigms.

### Data Representation

Python works with `Reservation` objects. Each reservation contains attributes such as customer ID, date, time, party size, and status.

Haskell represents reservations using records. Reservation lists are treated as immutable data and are passed into functions when processing is required.

### Searching and Filtering

Python mainly uses list comprehensions to search and filter reservations.

For example:

```python
[
    reservation
    for reservation in reservations
    if reservation.customer_id == customer_id
]
```

Haskell uses the higher-order function `filter`:

```haskell
filter
    (\reservation ->
        reservationCustomerId reservation == customerId
    )
    reservations
```

Both approaches achieve the same result, but the Haskell implementation expresses the operation as a functional transformation.

### Data Modification

The Python system follows an object-oriented design where objects and managers can maintain and update system state.

In contrast, the functions in `Search.hs` do not modify the original reservation list. They receive data and return a new result, which follows the functional programming principle of immutability.

### Daily Summary

Python uses familiar built-in operations such as `len()` and `sum()`.

Haskell combines several functions:

```haskell
filterByDate
length
map
sum
```

This demonstrates how complex processing can be built by composing smaller functions.

### Type Handling

Python uses strings to represent reservation status.

Haskell uses the `ReservationStatus` algebraic data type. This makes the possible reservation states more explicit and reduces the need to rely on arbitrary status strings inside the pure functions.

### Overall Comparison

Python is more direct for implementing a console-based reservation system because objects and attributes closely represent real-world entities such as customers, reservations, and tables.

Haskell requires a different way of thinking because data is generally transformed through pure functions rather than modified directly. However, functions such as `filter`, `map`, and `sortOn` make search and reporting operations concise and predictable.

Implementing the same Search and Reporting requirements in both languages demonstrates how an object-oriented approach and a functional approach can solve the same problem using different programming techniques.
