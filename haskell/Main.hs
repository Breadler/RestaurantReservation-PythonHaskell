module Main (main) where

import Control.Exception (ErrorCall (..), catch)
import Data.IORef
import Data.Time (Day, getCurrentTime, utctDay)
import Text.Read (readMaybe)

import Customer (viewCustomer)
import Reservation (cancelReservation, createReservation, updateReservation, viewReservation)
import Types (Customer, Reservation (..), ReservationStatus (..), Table)
import Validation (validateDate, validatePartySize, validateTime)

data AppState = AppState
  { customers         :: [Customer]
  , reservations      :: [Reservation]
  , tables            :: [Table]
  , nextReservationId :: Int
  }

initialState :: AppState
initialState = AppState
  { customers = []
  , reservations = []
  , tables = []
  , nextReservationId = 1
  }

main :: IO ()
main = newIORef initialState >>= loop

loop :: IORef AppState -> IO ()
loop stateRef = do
  putStrLn "\n=== Restaurant Reservation System ==="
  putStrLn "1. Customers"
  putStrLn "2. Reservations"
  putStrLn "3. Tables"
  putStrLn "4. Search & Reports"
  putStrLn "5. Exit"
  putStr "Choose an option: "
  choice <- getLine
  case choice of
    "1" -> putStrLn "Customer menu not implemented yet. (TODO Member 2)" >> loop stateRef
    "2" -> reservationMenu stateRef >> loop stateRef
    "3" -> putStrLn "Table menu not implemented yet. (TODO Member 3)" >> loop stateRef
    "4" -> putStrLn "Search & Reports menu not implemented yet. (TODO Member 4)" >> loop stateRef
    "5" -> putStrLn "Goodbye!"
    _   -> putStrLn "Invalid choice." >> loop stateRef

-- | Owner: Member 1. Reservation submenu -- create/view/update/cancel/list,
-- looping until "Back". Customer-existence and table-availability checks
-- happen here (not in Reservation.hs), same split as reservation_menu()
-- in python/main.py.
reservationMenu :: IORef AppState -> IO ()
reservationMenu stateRef = do
  putStrLn "\n--- Reservations ---"
  putStrLn "1. Create reservation"
  putStrLn "2. View reservation"
  putStrLn "3. Update reservation"
  putStrLn "4. Cancel reservation"
  putStrLn "5. List all reservations"
  putStrLn "6. Back"
  putStr "Choose an option: "
  choice <- getLine
  case choice of
    "1" -> runAction (createReservationPrompt stateRef) >> reservationMenu stateRef
    "2" -> runAction (viewReservationPrompt stateRef) >> reservationMenu stateRef
    "3" -> runAction (updateReservationPrompt stateRef) >> reservationMenu stateRef
    "4" -> runAction (cancelReservationPrompt stateRef) >> reservationMenu stateRef
    "5" -> runAction (listReservationsPrompt stateRef) >> reservationMenu stateRef
    "6" -> return ()
    _   -> putStrLn "Invalid choice." >> reservationMenu stateRef

-- | Other modules' unimplemented functions currently evaluate to
-- `error "TODO(Member N): ..."`. Catching that here keeps one missing
-- piece from crashing the whole program -- the Haskell counterpart of the
-- `except NotImplementedError` catch around action() in python/main.py's
-- run(). Deliberately narrow (only ErrorCall, not every exception) so real
-- bugs still surface loudly, matching how the Python side only catches
-- NotImplementedError/ValidationError and lets other exceptions propagate.
runAction :: IO () -> IO ()
runAction action = action `catch` handler
  where
    handler :: ErrorCall -> IO ()
    handler (ErrorCall msg) = putStrLn ("That part isn't implemented yet: " ++ msg)

-- | Pure: validates fields and builds a Reservation, or returns the first
-- validation error. Kept separate from the IO prompt below so the "what
-- makes a reservation valid" logic is testable without a terminal.
buildReservation
  :: Day -> Int -> Int -> Int -> String -> String -> Int -> Either String Reservation
buildReservation today rid custId tblId dateStr timeStr size = do
  date' <- validateDate today dateStr
  time' <- validateTime timeStr
  size' <- validatePartySize size
  Right Reservation
    { reservationId = rid
    , reservationCustomerId = custId
    , reservationTableId = tblId
    , reservationDate = date'
    , reservationTime = time'
    , partySize = size'
    , reservationStatus = Active
    }

createReservationPrompt :: IORef AppState -> IO ()
createReservationPrompt stateRef = do
  state <- readIORef stateRef
  putStr "Customer ID: "
  custIdInput <- getLine
  putStr "Table ID: "
  tableIdInput <- getLine
  putStr "Date (YYYY-MM-DD): "
  dateInput <- getLine
  putStr "Time (HH:MM): "
  timeInput <- getLine
  putStr "Party size: "
  sizeInput <- getLine
  case (readMaybe custIdInput, readMaybe tableIdInput, readMaybe sizeInput) of
    (Just custId, Just tblId, Just size) ->
      case viewCustomer custId (customers state) of
        Nothing -> putStrLn ("No customer with ID " ++ show custId ++ ".")
        Just _  -> do
          today <- utctDay <$> getCurrentTime
          case buildReservation today (nextReservationId state) custId tblId dateInput timeInput size of
            Left err -> putStrLn ("Invalid input: " ++ err)
            Right reservation -> do
              let updated = createReservation reservation (reservations state)
              writeIORef stateRef state
                { reservations = updated
                , nextReservationId = nextReservationId state + 1
                }
              putStrLn ("Created reservation #" ++ show (reservationId reservation) ++ ".")
    _ -> putStrLn "Customer ID, Table ID, and party size must be whole numbers."

viewReservationPrompt :: IORef AppState -> IO ()
viewReservationPrompt stateRef = do
  state <- readIORef stateRef
  putStr "Reservation ID: "
  input <- getLine
  case readMaybe input of
    Nothing -> putStrLn "Reservation ID must be a whole number."
    Just rid -> case viewReservation rid (reservations state) of
      Nothing -> putStrLn "Not found."
      Just r  -> print r

updateReservationPrompt :: IORef AppState -> IO ()
updateReservationPrompt stateRef = do
  state <- readIORef stateRef
  putStr "Reservation ID: "
  idInput <- getLine
  case readMaybe idInput of
    Nothing -> putStrLn "Reservation ID must be a whole number."
    Just rid ->
      case viewReservation rid (reservations state) of
        Nothing -> putStrLn "Not found."
        Just _  -> do
          putStr "Field to update (date/time/partysize): "
          field <- getLine
          putStr "New value: "
          value <- getLine
          today <- utctDay <$> getCurrentTime
          let result = case field of
                "date"      -> fmap (\d r -> r { reservationDate = d }) (validateDate today value)
                "time"      -> fmap (\t r -> r { reservationTime = t }) (validateTime value)
                "partysize" -> case readMaybe value of
                  Nothing -> Left "Party size must be a whole number."
                  Just sz -> fmap (\p r -> r { partySize = p }) (validatePartySize sz)
                _           -> Left ("Unknown field: " ++ field)
          case result of
            Left err       -> putStrLn ("Invalid input: " ++ err)
            Right updateFn -> do
              writeIORef stateRef state { reservations = updateReservation rid updateFn (reservations state) }
              putStrLn "Updated."

cancelReservationPrompt :: IORef AppState -> IO ()
cancelReservationPrompt stateRef = do
  state <- readIORef stateRef
  putStr "Reservation ID: "
  input <- getLine
  case readMaybe input of
    Nothing -> putStrLn "Reservation ID must be a whole number."
    Just rid ->
      case viewReservation rid (reservations state) of
        Nothing -> putStrLn "Not found."
        Just _  -> do
          writeIORef stateRef state { reservations = cancelReservation rid (reservations state) }
          putStrLn "Cancelled."

listReservationsPrompt :: IORef AppState -> IO ()
listReservationsPrompt stateRef = do
  state <- readIORef stateRef
  if null (reservations state)
    then putStrLn "No reservations yet."
    else mapM_ print (reservations state)
