module Table
  ( listAvailable
  , isDoubleBooked
  ) where

import Types (Reservation, Table)

-- | Owner: Member 3. See docs/modules/table.md for design notes,
-- implementation write-up, and test cases this module feeds into.

-- | Tables with no active reservation at the given date/time.
--
-- TODO(Member 3): a table is available if no reservation in the given list
-- has status Active with the same table ID, date, and time. Availability
-- is computed from reservations rather than a stored flag on Table, so the
-- two can never get out of sync.
listAvailable :: String -> String -> [Table] -> [Reservation] -> [Table]
listAvailable = error "TODO(Member 3): implement listAvailable"

-- | True if the table already has an active reservation at the given
-- date/time. This is the core invariant enforced before Reservation.hs
-- creates/updates a reservation.
isDoubleBooked :: Int -> String -> String -> [Reservation] -> Bool
isDoubleBooked = error "TODO(Member 3): implement isDoubleBooked"
