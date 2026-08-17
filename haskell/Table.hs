module Table
  ( listAvailable
  , isDoubleBooked
  ) where

import Types (Reservation (..), ReservationStatus (..), Table (..), TableStatus (..))

-- | Tables with no active reservation at the given date/time.
listAvailable :: String -> String -> [Table] -> [Reservation] -> [Table]
listAvailable date time tables reservations =
  filter
    (\tbl -> tableStatus tbl == Ready && not (isDoubleBooked (tableId tbl) date time reservations))
    tables

-- | True if the table already has an active reservation at the given date/time.
isDoubleBooked :: Int -> String -> String -> [Reservation] -> Bool
isDoubleBooked tableId date time reservations =
  any
    (\r -> reservationTableId r == tableId
      && reservationStatus r == Active
      && reservationDate r == date
      && reservationTime r == time)
    reservations
