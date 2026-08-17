## 1.0 Introduction

### 1.1 Background

Programming language concepts shape how software is structured, maintained, and extended. The same problem can be solved in many different ways depending on the paradigm a language encourages: an object-oriented language groups data and the operations on that data into classes and objects, while a functional language favours immutable data and pure functions that transform one value into another without side effects. Studying both approaches side by side, on the same problem, makes these differences concrete rather than theoretical.

Restaurant reservation management is a natural fit for this comparison. It requires simple data records (customers, tables, reservations), everyday CRUD operations, and one non-trivial business rule (preventing a table from being double-booked) that is small enough to implement cleanly in either paradigm but rich enough to show real differences in how the two paradigms express state and validation.

### 1.2 Problem Statement

Restaurants need a reliable way to record customer details, manage table bookings, and avoid scheduling conflicts, without relying on error-prone manual processes such as paper booking sheets or spreadsheets. At the same time, students learning multiple programming paradigms often study them in isolation and rarely get to see the same functional requirements implemented twice, once in each style, to compare directly.

This project addresses both: it is a working Restaurant Reservation System, and it is deliberately implemented twice, once in Python using Object-Oriented Programming and once in Haskell using Functional Programming, so the two implementations can be compared directly against identical requirements.

### 1.3 Project Objectives

- Develop a working Restaurant Reservation System covering customer management, reservation management, table management, and search/reporting.
- Implement the same functional requirements twice: once in Python (Object-Oriented Programming) and once in Haskell (Functional Programming).
- Apply core programming language concepts in both implementations: data types, functions/methods, control structures, modularity, scope, and input validation.
- Compare how each paradigm expresses state, validation, and data manipulation for the same problem.

### 1.4 Scope of the Project

The system supports:

- Customer management: add, view, update, and delete customer records.
- Reservation management: create, view, update, and cancel reservations, with validation of the reservation date, time, and party size.
- Table management: register tables, view availability for a given date and time, and prevent double-booking.
- Search and reporting: view all reservations, search by customer, filter by date or status, produce a daily summary, and sort reservations by date and time.

The system does not include a graphical user interface, persistent storage (all data is held in memory for the duration of a run), network or web access, or payment processing. Both implementations are console applications driven by a menu-based interface.

### 1.5 Report Organization

Chapter 2 presents the requirements analysis. Chapter 3 describes the system design, including the architecture, data structures, and diagrams shared by both implementations. Chapter 4 describes the implementation in each language. Chapter 5 presents the testing strategy, test cases, and results. Chapter 6 discusses and compares the two paradigms. Chapter 7 concludes the report and suggests future work.
