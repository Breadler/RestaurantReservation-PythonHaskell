module Types
  ( Customer(..)
  , Table(..)
  , TableStatus(..)
  , ReservationStatus(..)
  , Reservation(..)
  ) where

-- | A restaurant customer. Owner: Member 2.
data Customer = Customer
  { customerId    :: Int
  , customerName  :: String
  , customerPhone :: String
  , customerEmail :: String
  } deriving (Show, Eq)

-- | A restaurant table. Owner: Member 3.
data TableStatus = Ready | UnderMaintenance
  deriving (Show, Eq)

data Table = Table
  { tableId       :: Int
  , tableCapacity :: Int
  , tableStatus   :: TableStatus
  } deriving (Show, Eq)

-- | Owner: Member 1.
data ReservationStatus = Active | Cancelled
  deriving (Show, Eq)

-- | A reservation linking a customer to a table at a date/time. Owner: Member 1.
data Reservation = Reservation
  { reservationId         :: Int
  , reservationCustomerId :: Int
  , reservationTableId    :: Int
  , reservationDate       :: String -- YYYY-MM-DD, format-checked by Validation.validateDate
  , reservationTime       :: String -- HH:MM 24-hour, format-checked by Validation.validateTime
  , partySize             :: Int
  , reservationStatus     :: ReservationStatus
  } deriving (Show, Eq)
