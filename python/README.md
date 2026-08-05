# Python Implementation (OOP)

Plain scripts, no packages or dependencies beyond the standard library.

## Run
```
cd python
python main.py
```

## Layout
- `main.py` — menu-driven entry point.
- `customer.py` — Member 2 (Customer model + CustomerManager).
- `reservation.py` — Member 1 (Reservation model + ReservationManager).
- `table.py` — Member 3 (Table model + TableManager, double-booking check).
- `search.py` — Member 4 (search/filter/reporting).
- `validation.py` — shared input validation.

Each manager/function currently raises `NotImplementedError` — replace with real logic per your assigned module doc in [../docs/modules/](../docs/modules/). See [../docs/design/project-structure.md](../docs/design/project-structure.md) for the overall design.
