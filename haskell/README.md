# Haskell Implementation (FP)

Plain `.hs` files, no cabal/stack project needed — just GHC.

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
- `Main.hs` — menu-driven entry point.
- `Customer.hs` — Member 2.
- `Reservation.hs` — Member 1.
- `Table.hs` — Member 3 (availability, double-booking check).
- `Search.hs` — Member 4 (search/filter/reporting).
- `Validation.hs` — shared input validation.
- `Types.hs` — shared data types.

Each function currently evaluates `error "TODO..."` — replace with real logic per your assigned module doc in [../docs/modules/](../docs/modules/). See [../docs/design/project-structure.md](../docs/design/project-structure.md) for the overall design.
