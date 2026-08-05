module Reservation
  ( createReservation
  , viewReservation
  , updateReservation
  , cancelReservation
  ) where

import Data.List (find)

import Types (Reservation (..), ReservationStatus (..))

-- | Owner: Member 1. See docs/modules/reservation.md for design notes,
-- implementation write-up, and test cases this module feeds into.
--
-- This module only knows how to fold a `Reservation` into/out of a
-- `[Reservation]` list. Validation (Validation.hs) and cross-module checks
-- (customer exists, table free) are the caller's job (Main.hs) -- same
-- separation of concerns as reservation.py, so the two implementations
-- stay comparable.

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

-- | Mark a reservation as cancelled, returning the updated list. Status
-- changes go through this function rather than updateReservation's
-- generic field-update, matching "Update" and "Cancel" being separate
-- operations in the system requirements.
cancelReservation :: Int -> [Reservation] -> [Reservation]
cancelReservation rid = updateReservation rid (\r -> r { reservationStatus = Cancelled })
