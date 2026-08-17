# Haskell Implementation (FP)

Plain `.hs` files, no cabal/stack project needed, just GHC.

## Setup
Install GHC (e.g. via [GHCup](https://www.haskell.org/ghcup/)).

## Run
```
cd haskell
runghc Main.hs
```

## Compile (optional)
```
cd haskell
ghc Main.hs -o restaurant-reservation
./restaurant-reservation
```

## Layout
- `Main.hs`: menu-driven entry point and application state.
- `Types.hs`: shared data types (Customer, Table, Reservation).
- `Customer.hs`: customer operations (add, view, update, delete).
- `Reservation.hs`: reservation operations (create, view, update, cancel).
- `Table.hs`: availability and double-booking check.
- `Search.hs`: search, filter, and reporting over reservations.
- `Validation.hs`: shared input validation.
- `SearchTest.hs`: standalone manual test harness for `Search.hs`; run with `runghc SearchTest.hs`.

See [../docs/design/project-structure.md](../docs/design/project-structure.md) for the overall design.
