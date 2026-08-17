TITLE PAGE
Restaurant Reservation System (Python & Haskell)
Programming Language Concepts Project Report
Course: [Course Code and Course Name]
Lecturer: [Lecturer Name]
Group Members:
1.	[Student Name] – [Student ID]
2.	[Student Name] – [Student ID]
3.	[Student Name] – [Student ID]
4.	[Student Name] – [Student ID]
Submission Date: [DD Month YYYY]
________________________________________
DECLARATION
We declare that this report and the accompanying project work are entirely our own work and that all sources used have been properly acknowledged.

ABSTRACT
This project presents the Restaurant Reservation System, developed to compare Object-Oriented Programming (Python) and Functional Programming (Haskell) in solving the same problem. The system manages customers, reservations, and restaurant tables: staff can add, view, update, and delete customer and reservation records, manage tables while preventing double bookings, and search, filter, and report on reservations. The same functionality is implemented independently in both languages. This report covers the problem, requirements, design, implementation, testing, and a comparison of the two paradigms; the two implementations produce equivalent results from identical input, while differing substantially in how they represent and update state.

Keywords: Restaurant Reservation, Object-Oriented Programming, Functional Programming, Python, Haskell
________________________________________
TABLE OF CONTENTS

1. [Introduction](report/01-introduction.md)
2. [Requirements Analysis](report/02-requirements-analysis.md)
3. [Design](report/03-design.md)
4. [Implementation](report/04-implementation.md)
5. [Testing and Results](report/05-testing-and-results.md)
6. [Discussion](report/06-discussion.md)
7. [Conclusion](report/07-conclusion.md)
8. [References](report/08-references.md)
9. [Appendices](report/09-appendices.md)

________________________________________
LIST OF FIGURES

- Figure 3.1: High-level architecture
- Figure 3.2: Data relationship
- Figure 3.3: Python class diagram (OOP)
- Figure 3.4: Haskell module / type diagram (FP)
- Figure 3.5: Main menu flowchart
- Figure 3.6: Create-reservation flow (validation and double-booking check)
- Figure 4.1: Main menu
- Figure 4.2: Successful reservation creation (Python)
- Figure 4.3: Successful reservation creation (Haskell)
- Figure 5.1: Rejecting a reservation against a nonexistent table (Python)
- Figure 5.2: Rejecting a double-booked reservation (Haskell)
- Figure 5.3: Daily summary output

________________________________________
LIST OF TABLES

- Table 5.1: Customer Management test cases
- Table 5.2: Reservation Management test cases
- Table 5.3: Table Management test cases
- Table 5.4: Search & Reporting test cases
- Table B.1: Group contribution (Appendix B)

________________________________________

This report is organised as separate chapter files under [report/](report/). See the Table of Contents above.
