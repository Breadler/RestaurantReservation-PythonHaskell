module Validation
  ( validateNonEmpty
  , validatePhone
  , validateEmail
  , validateDate
  , validateTime
  , validatePartySize
  ) where

import Data.Time (Day, TimeOfDay, defaultTimeLocale, parseTimeM)

-- | Owner: whole group. Each validator returns Left with an error message
-- on invalid input, or Right with the validated value.

-- TODO(Member 2): implement validateNonEmpty
validateNonEmpty :: String -> String -> Either String String
validateNonEmpty = error "TODO: implement validateNonEmpty"

-- TODO(Member 2): implement validatePhone
validatePhone :: String -> Either String String
validatePhone = error "TODO: implement validatePhone"

-- TODO(Member 2): implement validateEmail
validateEmail :: String -> Either String String
validateEmail = error "TODO: implement validateEmail"

-- | Owner: Member 1. `today` is passed in rather than fetched with
-- `getCurrentTime` inside this function, so the validator stays pure and
-- easy to test -- the IO boundary (reading the clock) lives in Main.hs.
validateDate :: Day -> String -> Either String String
validateDate today value =
  case parseTimeM True defaultTimeLocale "%Y-%m-%d" value :: Maybe Day of
    Nothing -> Left (value ++ " is not a valid date (expected YYYY-MM-DD).")
    Just d
      | d < today -> Left ("Reservation date " ++ value ++ " is in the past.")
      | otherwise -> Right value

-- | Owner: Member 1.
validateTime :: String -> Either String String
validateTime value =
  case parseTimeM True defaultTimeLocale "%H:%M" value :: Maybe TimeOfDay of
    Nothing -> Left (value ++ " is not a valid time (expected HH:MM, 24-hour).")
    Just _  -> Right value

-- | Owner: Member 1.
validatePartySize :: Int -> Either String Int
validatePartySize value
  | value <= 0 = Left "Party size must be at least 1."
  | otherwise  = Right value
