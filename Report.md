
WORKING DOCUMENTS
This report is being assembled from separate working files so each member can update their own section independently. Before final submission, merge the linked content below into the relevant chapters of this file.
•	Project structure & diagrams (shared): docs/design/project-structure.md
•	Reservation module (Member 1): docs/modules/reservation.md
•	Customer module (Member 2): docs/modules/customer.md
•	Table module (Member 3): docs/modules/table.md
•	Search & Reporting module (Member 4): docs/modules/search-reporting.md
________________________________________
TITLE PAGE
Restaurant Reservation System (Python & Haskell)
Programming Language Concepts Project Report
Course: [Course Code and Course Name]
Lecturer: [Lecturer Name]
Group Members:
1.	[Student Name] – [Student ID] – Reservation Management
2.	[Student Name] – [Student ID] – Customer Management
3.	[Student Name] – [Student ID] – Table Management
4.	[Student Name] – [Student ID] – Search & Reporting
Submission Date: [DD Month YYYY]
________________________________________
DECLARATION
We declare that this report and the accompanying project work are entirely our own work and that all sources used have been properly acknowledged.
ABSTRACT
This project presents the Restaurant Reservation System, developed to compare Object-Oriented Programming (Python) and Functional Programming (Haskell) in solving the same problem. The system manages customers, reservations, and restaurant tables, allowing staff to add, view, update, and delete customer and reservation records, assign tables while preventing double bookings, and search or filter reservations. The report discusses the problem, requirements, design, implementation, testing, and comparison of the two paradigms. The findings show that while both implementations provide identical functionality, they differ significantly in structure, state handling, and code organization.
Keywords: Restaurant Reservation, Object-Oriented Programming, Functional Programming, Python, Haskell
________________________________________
TABLE OF CONTENTS
[Insert automatic table of contents here]
________________________________________
LIST OF FIGURES
[Insert list of figures here]
________________________________________
LIST OF TABLES
[Insert list of tables here]
________________________________________
1.0 INTRODUCTION
1.1 Background
Programming language concepts are important because they influence how software is structured, maintained, and extended. Restaurants commonly rely on reservation systems to manage bookings, avoid scheduling conflicts, and keep track of customer information. Building the same reservation system in two different paradigms allows a direct comparison of how each paradigm approaches state management, data modeling, and control flow.
1.2 Problem Statement
Students often learn programming paradigms separately and do not clearly see how the same problem can be implemented differently in each paradigm. Restaurants also need a simple, reliable way to manage customers, reservations, and tables without double-booking or losing track of customer details. This project addresses both issues by building one reservation system twice — once in Python (OOP) and once in Haskell (FP) — to make the paradigm differences concrete.
1.3 Project Objectives
•	To develop a working Restaurant Reservation System.
•	To compare Object-Oriented Programming and Functional Programming as applied to the same problem domain.
•	To apply programming language concepts such as data types, functions/methods, control structures, modules, scope, input validation, and data manipulation in both paradigms.
•	To ensure both implementations provide equivalent functionality so the paradigms can be fairly compared.
1.4 Scope of the Project
The system supports customer management (add, view, update, delete), reservation management (create, view, update, cancel), and table management (display availability, assign tables, prevent double booking), along with search and reporting features (view all, search, filter, and optional daily summary/sorting). It does not include a graphical user interface, persistent database storage, online/web access, or payment processing — data is expected to be held in memory or simple local storage for the duration of the program's use.
1.5 Report Organization
Chapter 2 presents the requirements analysis, Chapter 3 explains the design, Chapter 4 describes the implementation, Chapter 5 presents testing, Chapter 6 discusses the findings, and Chapter 7 concludes the report.
________________________________________
2.0 REQUIREMENTS ANALYSIS
2.1 Project Description
This project is a Restaurant Reservation System that manages customers, reservations, and tables for a restaurant, implemented independently in Python (OOP) and Haskell (FP).
2.2 Functional Requirements
Customer Management
•	Add customer
•	View customer
•	Update customer
•	Delete customer
Reservation Management
•	Create reservation
•	View reservation
•	Update reservation
•	Cancel reservation
Table Management
•	Display available tables
•	Assign tables to reservations
•	Prevent double booking
Search & Reporting
•	View all reservations
•	Search reservations
•	Filter reservations
•	Daily reservation summary (optional)
•	Sorting (optional)
Input Validation
•	Validate customer information
•	Validate reservation date and time
•	Prevent invalid or incomplete input
2.3 Non-Functional Requirements
•	The program must be easy to use via a menu-driven interface.
•	The code must be modular and readable in both Python and Haskell.
•	All user input must be validated before being processed.
•	The system must run without errors and handle invalid input gracefully.
•	Both implementations must provide the same functionality for a fair comparison.
2.4 Paradigm Comparison Requirements
The project compares how the same reservation system is represented in Object-Oriented Programming (Python) and Functional Programming (Haskell), focusing on data structure design, state management (mutable objects vs. immutable data), function/method organization, and overall readability and maintainability.
2.5 User Requirements
The intended users are restaurant staff (e.g., hosts or managers) who need to manage customer records, reservations, and table assignments for the restaurant.
________________________________________
3.0 DESIGN
3.1 System Overview
The system uses a menu-driven console interface and contains two independent versions of the same application logic: an Object-Oriented version in Python and a Functional version in Haskell. Both versions expose the same four core modules: Customer Management, Reservation Management, Table Management, and Search & Reporting.
3.2 Architecture / Module Structure
•	Main menu module
•	Input validation module
•	Customer management module
•	Reservation management module
•	Table management module
•	Search & reporting module
Each module is implemented once per language as a single flat file, mapped 1:1 to a group member (e.g. `python/reservation.py` / `haskell/Reservation.hs` for Member 1). The code is deliberately minimal (plain scripts/modules, no build tooling) so the group's effort goes into the paradigm comparison rather than project scaffolding. The full repository layout, module-to-owner map, and architecture diagram are maintained in docs/design/project-structure.md and should be pasted in here (or exported as a figure) for the final submission.
3.3 Data Structures Used
In the Python (OOP) version, customers, reservations, and tables are represented as classes/objects stored in collections (e.g., lists or dictionaries) managed by manager classes. In the Haskell (FP) version, customers, reservations, and tables are represented as immutable data types (e.g., records via `data`), with collections passed through and returned from pure functions rather than mutated in place. See the ER-style data relationship diagram and the Haskell module/type diagram in docs/design/project-structure.md.
3.4 Flowchart / Pseudocode / Class Diagram
Figure 3.1 (Main Menu Flowchart): the program repeatedly presents Customers / Reservations / Tables / Search & Reports / Exit until exit is selected.
Figure 3.2 (Create-Reservation Flow): shows the validation and double-booking check performed before a reservation is created — this is the system's core invariant and should be explained in detail in the Table module discussion.
Figure 3.3: Python class diagram (OOP).
Figure 3.4: Haskell module/type diagram (FP).
All four diagrams are drafted in text form in docs/design/project-structure.md and should be pasted in here (or redrawn as images/figures) for the final submission.
3.5 Input and Output Design
Input includes customer details (name, contact info), reservation details (date, time, party size, linked customer), and table details (table number, capacity). Output includes confirmation messages, validation/error messages, reservation and customer listings, table availability displays, and search/filter results.
3.6 Design Notes for Paradigm 1 – Python (OOP)
The object-oriented design uses classes such as `Customer`, `Reservation`, `Table`, and corresponding manager classes to group data and behavior together, using encapsulation to manage state and methods to perform CRUD operations.
3.7 Design Notes for Paradigm 2 – Haskell (FP)
The functional design uses immutable data types and pure functions to model customers, reservations, and tables. State changes (e.g., adding a reservation) are handled by producing new data structures rather than mutating existing ones, with I/O isolated in the `IO` monad at the program's boundary.
________________________________________
4.0 IMPLEMENTATION
4.1 Tools and Language Used
The project was developed using Python and Haskell (GHC), with [Visual Studio Code / other IDE] as the development environment.
4.2 Implementation of Paradigm 1 – Python (OOP)
The object-oriented version uses classes such as `Customer`, `Reservation`, `Table`, `CustomerManager`, `ReservationManager`, and `TableManager`, with methods such as `add_customer()`, `create_reservation()`, and `assign_table()`. Detailed per-module implementation notes and code extracts are written by each owner in their working file and should be merged in here before submission: docs/modules/reservation.md, docs/modules/customer.md, docs/modules/table.md, docs/modules/search-reporting.md.
4.3 Implementation of Paradigm 2 – Haskell (FP)
The functional version uses data types such as `Customer`, `Reservation`, and `Table`, with pure functions such as `addCustomer`, `createReservation`, and `assignTable` that return updated copies of the data rather than mutating it. Detailed per-module implementation notes and code extracts are written by each owner in their working file (same links as section 4.2) and should be merged in here before submission.
4.4 Key Language Concepts Applied
This project demonstrates variables, control structures, parameter passing, scope rules, and modularity in both languages, along with object-oriented concepts such as encapsulation and class design in Python, and functional concepts such as immutability, pure functions, pattern matching, and recursion in Haskell.
4.5 Code Organization
The source code for each language is divided into separate modules/files (e.g., customer, reservation, table, and search/reporting modules) to improve readability and maintainability, matching the task distribution among group members.
4.6 Sample Screenshots or Code Extracts
[Insert selected screenshots or code snippets.]
Sample:
Figure 4.1 shows the main menu output when the system starts.
________________________________________
5.0 TESTING AND RESULTS
5.1 Testing Strategy
The system was tested using normal input, invalid input, empty input, and boundary cases, including double-booking attempts and invalid reservation dates/times, in both the Python and Haskell implementations.
5.2 Test Cases
Test ID	Test Description	Input	Expected Result	Actual Result	Status
TC01	Add valid customer	[Input]	[Expected]	[Actual]	[Pass/Fail]
TC02	Create valid reservation	[Input]	[Expected]	[Actual]	[Pass/Fail]
TC03	Prevent double booking	[Input]	[Expected]	[Actual]	[Pass/Fail]
TC04	Invalid reservation date/time	[Input]	[Expected]	[Actual]	[Pass/Fail]
TC05	Update existing customer	[Input]	[Expected]	[Actual]	[Pass/Fail]
TC06	Cancel reservation	[Input]	[Expected]	[Actual]	[Pass/Fail]
Full, per-module test case tables (IDs prefixed RES/CUST/TBL/SR) are maintained by each owner and should be merged into the table above before submission: docs/modules/reservation.md, docs/modules/customer.md, docs/modules/table.md, docs/modules/search-reporting.md.
5.3 Error and Edge Cases
The system was tested with duplicate customer records, missing required fields, overlapping table bookings, and invalid date/time formats to ensure validation messages were displayed correctly in both implementations.
5.4 Testing Evidence
[Insert screenshots, console outputs, or logs.]
Sample:
Figure 5.1 shows the system response after attempting to double-book a table.
5.5 Results Summary
[Summarize the testing outcome after development and testing are complete.]
________________________________________
6.0 DISCUSSION
6.1 Comparison of the Two Paradigms
[Discuss the differences between the Python (OOP) and Haskell (FP) implementations after development is complete. Draw from each owner's "Module-Specific Discussion" subsection in docs/modules/reservation.md, docs/modules/customer.md, docs/modules/table.md, and docs/modules/search-reporting.md, then synthesize a single cross-module comparison here.]
6.2 Analysis of Programming Language Concepts
[Connect the project to course topics, e.g., how scope, types, parameter passing, and abstraction/immutability affected program design and implementation.]
6.3 Strengths and Limitations
[Discuss strengths and weaknesses of each implementation, e.g., Python's ease of modeling mutable state vs. Haskell's guarantees around immutability and correctness.]
6.4 Lessons Learned
[State what the group learned about paradigm differences after completing the project.]
________________________________________
7.0 CONCLUSION
7.1 Conclusion
[Give the final conclusion of the project after development and testing are complete.]
7.2 Future Work
Future improvements may include database integration, a graphical user interface, online/web access, and data export features.
________________________________________
REFERENCES
•	Sebesta, R. W. Concepts of Programming Languages.
•	Python Software Foundation. Python Documentation.
•	Haskell.org. The Haskell Programming Language Documentation.
•	[Any additional article, textbook, or website used]
________________________________________
APPENDICES
Appendix A: Full Source Code
[Paste or attach the full Python and Haskell source code here.]
Appendix B: Group Contribution
Member	Contribution
Member 1	Reservation Management (Python & Haskell): Create, View, Update, Cancel Reservation, Reservation validation; report sections for Reservation module (Python & Haskell)
Member 2	Customer Management (Python & Haskell): Add, View, Update, Delete Customer, Customer validation; report sections for Customer module (Python & Haskell)
Member 3	Table Management (Python & Haskell): Display available tables, Assign tables to reservations, Prevent double booking, Table management functions; report sections for Table Management module (Python & Haskell)
Member 4	Search & Reporting (Python & Haskell): View all reservations, Search reservations, Filter reservations, Daily reservation summary (optional), Sorting (optional); report sections for Search and Reporting module (Python & Haskell)
