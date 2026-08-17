## 7.0 Conclusion

### 7.1 Conclusion

This project set out to build a working Restaurant Reservation System twice, once in Python using Object-Oriented Programming and once in Haskell using Functional Programming, against the same requirements, so the two paradigms could be compared directly rather than studied separately. Both implementations provide the same functionality: managing customers, reservations, and tables; preventing double-booked tables; validating user input; and searching and reporting on reservations. Testing both implementations against the same inputs confirmed that they produce equivalent results, while the underlying code reflects two genuinely different ways of solving the same problem: mutable, encapsulated objects in Python versus immutable data and pure functions threaded through a single point of state in Haskell.

### 7.2 Future Work

Future improvements could include persistent storage (writing customers, reservations, and tables to a file or database so data survives between runs), a graphical or web-based interface in place of the console menu, and richer table management such as automatically checking party size against table capacity when assigning a table.
