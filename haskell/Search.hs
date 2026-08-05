module Search
  ( searchByCustomer
  , filterByDate
  , filterByStatus
  , dailySummary
  , sortByTime
  ) where

import Types (Reservation, ReservationStatus)

-- | Owner: Member 4. See docs/modules/search-reporting.md for design
-- notes, implementation write-up, and test cases this module feeds into.

searchByCustomer :: Int -> [Reservation] -> [Reservation]
searchByCustomer = error "TODO(Member 4): implement searchByCustomer"

filterByDate :: String -> [Reservation] -> [Reservation]
filterByDate = error "TODO(Member 4): implement filterByDate"

filterByStatus :: ReservationStatus -> [Reservation] -> [Reservation]
filterByStatus = error "TODO(Member 4): implement filterByStatus"

-- | Optional: total reservations and total guests for a given date.
dailySummary :: String -> [Reservation] -> (Int, Int)
dailySummary = error "TODO(Member 4): implement dailySummary (optional)"

-- | Optional: sort reservations by date then time.
sortByTime :: [Reservation] -> [Reservation]
sortByTime = error "TODO(Member 4): implement sortByTime (optional)"
