module Main where

import Search
import Types


r1 :: Reservation
r1 = Reservation
    { reservationId = 1
    , reservationCustomerId = 1
    , reservationTableId = 1
    , reservationDate = "2026-08-20"
    , reservationTime = "18:00"
    , partySize = 2
    , reservationStatus = Active
    }


r2 :: Reservation
r2 = Reservation
    { reservationId = 2
    , reservationCustomerId = 2
    , reservationTableId = 2
    , reservationDate = "2026-08-20"
    , reservationTime = "12:00"
    , partySize = 4
    , reservationStatus = Active
    }


r3 :: Reservation
r3 = Reservation
    { reservationId = 3
    , reservationCustomerId = 1
    , reservationTableId = 3
    , reservationDate = "2026-08-21"
    , reservationTime = "20:00"
    , partySize = 3
    , reservationStatus = Cancelled
    }


r4 :: Reservation
r4 = Reservation
    { reservationId = 4
    , reservationCustomerId = 3
    , reservationTableId = 1
    , reservationDate = "2026-08-20"
    , reservationTime = "19:30"
    , partySize = 5
    , reservationStatus = Active
    }


testReservations :: [Reservation]
testReservations = [r1, r2, r3, r4]


main :: IO ()
main = do
    putStrLn "\n=== Member 4 Search & Reporting Tests ==="

    putStrLn "\nSR-01: View all reservations"
    mapM_ print testReservations

    putStrLn "\nSR-02: Search by Customer ID = 1"
    mapM_ print (searchByCustomer 1 testReservations)

    putStrLn "\nSR-03: Filter by Date = 2026-08-20"
    mapM_ print (filterByDate "2026-08-20" testReservations)

    putStrLn "\nSR-04: Filter by Status = Cancelled"
    mapM_ print (filterByStatus Cancelled testReservations)

    putStrLn "\nSR-05: Daily Summary for 2026-08-20"
    print (dailySummary "2026-08-20" testReservations)

    putStrLn "\nSR-06: Sort by Date/Time"
    mapM_ print (sortByTime testReservations)