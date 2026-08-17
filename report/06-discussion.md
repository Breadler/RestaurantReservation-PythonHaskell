## 6.0 Discussion

### 6.1 Comparison of the Two Paradigms

Both implementations provide identical functionality, but arrive at it through very different means.

**State and mutation.** In Python, each functional area is owned by a manager class (`CustomerManager`, `ReservationManager`, `TableManager`) that holds a dictionary of records and mutates it directly: adding a customer inserts into the dictionary, updating a reservation calls `setattr` on the stored object, and deleting removes a key. State is encapsulated inside the object and changes in place. In Haskell, there are no manager objects: `Customer.hs`, `Reservation.hs`, and `Table.hs` are collections of pure functions of the form `[Record] -> ... -> [Record]`, each returning a new list rather than modifying an existing one. The only mutable state in the entire Haskell program is a single `IORef` in `Main.hs` holding the current customers, reservations, tables, and ID counters; every other function in the program is pure and has no notion of "before" and "after."

**Representing change as a value.** This difference is clearest in how the two languages handle updates. Python's `update()` methods take keyword arguments (`update(id, phone="555-1234")`) and mutate the matching field directly. Haskell's `updateCustomer`/`updateReservation` instead take the *change itself* as a function argument (`Customer -> Customer`), and apply it to whichever record matches the given ID:

```haskell
updateCustomer :: Int -> (Customer -> Customer) -> [Customer] -> [Customer]
```

Because "the update" is an ordinary value in Haskell, `cancelReservation` can be defined as nothing more than `updateReservation` applied to one specific function, rather than as separate logic:

```haskell
cancelReservation rid = updateReservation rid (\r -> r { reservationStatus = Cancelled })
```

Python's `cancel()` exists as its own method for the same behaviour, because there is no equally lightweight way to pass "the change to make" around as a value without writing a small function object.

**Error handling.** Python raises `ValidationError` (a subclass of the built-in `ValueError`) from deep inside a manager method, and the menu layer catches it several calls up the stack; the type system does not track which functions can raise, so this relies on the programmer knowing where errors can come from and remembering to catch them. Haskell's validators return `Either String a` (`Left` with a message on failure, `Right` with the value on success), which the compiler forces the caller to handle explicitly before the value inside can be used at all:

```haskell
validateDate :: Day -> String -> Either String String
```

The trade-off is verbosity versus guarantees: Python's exceptions are quick to write and read almost like plain English, while Haskell's `Either` makes every possible failure visible in the function's type signature, at the cost of more explicit plumbing (`case ... of Left ... -> ...; Right ... -> ...`) at each call site.

**Purity and the boundary with the outside world.** `validate_date` in Python simply calls `date.today()` internally to compare against the input. Haskell's `validateDate` cannot do this and stay pure, so it instead takes the current date as an explicit argument, with the one place that actually reads the system clock (`getCurrentTime`) living in `Main.hs`, right where the result is needed. This is a small example of a broader Haskell habit: keep as much logic as possible pure, and push anything that touches the outside world (the clock, the console) to the edges of the program.

**Search and reporting.** Python expresses filtering and aggregation with list comprehensions and built-ins (`sum(r.party_size for r in reservations)`); Haskell expresses the same operations with higher-order functions (`sum (map partySize reservations)`, `sortOn`, `filter`). Both read naturally in their respective language, and produce identical results on identical input, which is itself a useful observation: very different-looking code can implement exactly the same specification.

### 6.2 Analysis of Programming Language Concepts

The project demonstrates how a paradigm's core commitments ripple through an entire codebase. Object-oriented encapsulation (binding a table of records and the operations on it into one class) makes Python's managers easy to use (call a method, the object updates itself) but means nothing in the type system prevents two different call sites from mutating the same object in surprising ways. Functional immutability removes that risk entirely (a `Customer` value, once built, can never change under you), at the cost of needing an explicit place (here, a single `IORef`) to hold whatever *does* need to change over the life of the program. Similarly, Python's dynamic typing lets `update(id, **fields)` accept arbitrary keyword arguments checked at run time, while Haskell's static types push the equivalent design toward passing an explicit `Record -> Record` function, checked at compile time.

### 6.3 Strengths and Limitations

Python's object-oriented style is quick to write and reads naturally for anyone familiar with everyday procedural code: a manager class with `add`/`view`/`update`/`delete` methods is an immediately recognisable shape. Its main limitation here is that nothing stops a caller from mutating a record in a way that was not intended, since validation is only enforced at the points that happen to call it.

Haskell's functional style guarantees that existing data can never be silently changed elsewhere in the program, and its type signatures document exactly what a function needs and can fail on. Its main limitation is more ceremony for simple tasks (building a valid `Reservation` from raw strings, for example, needs an explicit `Either`-chaining function rather than a few sequential assignments) and a steeper learning curve for anyone coming from an imperative background.

### 6.4 Lessons Learned

Building the same requirements twice made the practical consequences of each paradigm's design concrete rather than abstract. The clearest lesson was that immutability is not just a restriction; it is also a design tool: once mutable state is confined to one place (a single `IORef`), everything else in the Haskell program becomes trivially safe to reason about and test in isolation, simply by calling it with a list and checking the list it returns. The corresponding lesson on the Python side was that OOP's convenience comes from trusting the object to protect its own invariants, which works well as long as every mutation genuinely goes through the object's own methods.
