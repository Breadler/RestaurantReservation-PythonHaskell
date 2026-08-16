module Search
  ( searchByCustomer
  , filterByDate
  , filterByStatus
  , dailySummary
  , sortByTime
  ) where

import Types (Reservation(..), ReservationStatus(..))
import Data.List (sortOn)

-- | Owner: Member 4. See docs/modules/search-reporting.md for design
-- notes, implementation write-up, and test cases this module feeds into.

searchByCustomer :: Int -> [Reservation] -> [Reservation]
searchByCustomer customerId reservations =
    filter
        (\reservation ->
            reservationCustomerId reservation == customerId
        )
        reservations

filterByDate :: String -> [Reservation] -> [Reservation]
filterByDate date reservations =
    filter
        (\reservation ->
            reservationDate reservation == date
        )
        reservations

filterByStatus :: ReservationStatus -> [Reservation] -> [Reservation]
filterByStatus status reservations =
    filter
        (\reservation ->
            reservationStatus reservation == status
        )
        reservations

-- | Optional: total reservations and total guests for a given date.
dailySummary :: String -> [Reservation] -> (Int, Int)
dailySummary date reservations =
    let dailyReservations = filterByDate date reservations
        totalReservations = length dailyReservations
        totalGuests = sum (map partySize dailyReservations)
    in
        (totalReservations, totalGuests)

-- | Optional: sort reservations by date then time.
sortByTime :: [Reservation] -> [Reservation]
sortByTime reservations =
    sortOn
        (\reservation ->
            (reservationDate reservation, reservationTime reservation)
        )
        reservations
