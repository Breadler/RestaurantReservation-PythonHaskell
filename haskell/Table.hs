module Table
  ( listAvailable
  , isDoubleBooked
  ) where

import Types (Reservation (..), ReservationStatus (..), Table (..), TableStatus (..))

-- | Owner: Member 3. See docs/modules/table.md for design notes,
-- implementation write-up, and test cases this module feeds into.

-- | Tables with no active reservation at the given date/time.
--
-- Availability is computed from reservations rather than a stored flag on
-- Table, so the two can never get out of sync.
listAvailable :: String -> String -> [Table] -> [Reservation] -> [Table]
listAvailable date time tables reservations =
  filter
    (\tbl -> tableStatus tbl == Ready && not (isDoubleBooked (tableId tbl) date time reservations))
    tables

-- | True if the table already has an active reservation at the given
-- date/time. This is the core invariant enforced before Reservation.hs
-- creates/updates a reservation.
isDoubleBooked :: Int -> String -> String -> [Reservation] -> Bool
isDoubleBooked tableId date time reservations =
  any
    (\r -> reservationTableId r == tableId
      && reservationStatus r == Active
      && reservationDate r == date
      && reservationTime r == time)
    reservations
