module Reservation
  ( createReservation
  , viewReservation
  , updateReservation
  , cancelReservation
  ) where

import Data.List (find)

import Types (Reservation (..), ReservationStatus (..))

-- | Add a new reservation, returning the updated list.
createReservation :: Reservation -> [Reservation] -> [Reservation]
createReservation reservation reservations = reservations ++ [reservation]

-- | Find a reservation by ID.
viewReservation :: Int -> [Reservation] -> Maybe Reservation
viewReservation rid = find ((== rid) . reservationId)

-- | Apply an update function to the reservation with the given ID,
-- returning the updated list unchanged if no reservation has that ID.
updateReservation :: Int -> (Reservation -> Reservation) -> [Reservation] -> [Reservation]
updateReservation rid f = map apply
  where
    apply r
      | reservationId r == rid = f r
      | otherwise               = r

-- | Mark a reservation as cancelled, returning the updated list.
cancelReservation :: Int -> [Reservation] -> [Reservation]
cancelReservation rid = updateReservation rid (\r -> r { reservationStatus = Cancelled })
