## 2.0 Requirements Analysis

### 2.1 Project Description

The system is a console-based Restaurant Reservation System that manages customers, reservations, and tables for a single restaurant. It is implemented twice, independently, in Python (Object-Oriented Programming) and Haskell (Functional Programming), against the same functional requirements.

### 2.2 Functional Requirements

**Customer Management**
- Add a customer (name, phone number, email address).
- View a customer by ID.
- Update a customer's name, phone number, or email address.
- Delete a customer.
- List all customers.

**Reservation Management**
- Create a reservation for a customer at a table, date, time, and party size.
- View a reservation by ID.
- Update a reservation's date, time, party size, or table.
- Cancel a reservation.
- List all reservations.

**Table Management**
- Add a table with a given seating capacity.
- View all tables and their status.
- Check which tables are available for a given date and time.
- Update a table's capacity or status (Active / Under Maintenance).
- Prevent a table from being double-booked at the same date and time.

**Search & Reporting**
- View all reservations.
- Search reservations by customer.
- Filter reservations by date.
- Filter reservations by status (active / cancelled).
- Produce a daily summary (total reservations and total guests for a date).
- Sort reservations by date and time.

**Input Validation**
- Customer name must not be empty.
- Phone number must contain between 7 and 15 digits (with optional formatting characters such as `+`, `-`, spaces, and parentheses).
- Email address must match a standard `user@domain.tld` structure.
- Reservation date must be a valid calendar date in `YYYY-MM-DD` format and not in the past.
- Reservation time must be a valid time in `HH:MM` 24-hour format.
- Party size must be a positive whole number.
- A reservation cannot be created against a table that does not exist, is under maintenance, or is already booked for that date and time.

### 2.3 Non-Functional Requirements

- The program is operated through a clear, menu-driven console interface.
- The two implementations provide identical functionality so they can be fairly compared.
- The code is organised into small, single-purpose modules rather than one large file.
- All user input is validated before being used, with clear error messages on invalid input.
- Invalid input (bad menu choices, malformed numbers, unknown fields) is handled without the program crashing.

### 2.4 Paradigm Comparison Requirements

Because the same system is built twice, the project also compares how Object-Oriented Programming (Python) and Functional Programming (Haskell) approach the same problem: how each represents data (mutable objects vs. immutable records), how each represents change over time (in-place mutation vs. producing new values), how each expresses validation (exceptions vs. `Either`), and how readable and maintainable the resulting code is in each style.

### 2.5 User Requirements

The intended user is restaurant staff (a host, waiter, or manager) who needs a simple tool to record customer details, manage table bookings for the day, and check availability before confirming a booking, without needing any technical training beyond following an on-screen menu.
