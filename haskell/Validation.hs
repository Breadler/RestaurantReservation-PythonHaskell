module Validation
  ( validateNonEmpty
  , validatePhone
  , validateEmail
  , validateDate
  , validateTime
  , validatePartySize
  ) where

import Data.Char (isAlphaNum, isDigit, isSpace)
import Data.List (isPrefixOf, isSuffixOf)
import Data.Time (Day, TimeOfDay, defaultTimeLocale, parseTimeM)

-- | Owner: whole group. Each validator returns Left with an error message
-- on invalid input, or Right with the validated value.

-- | Helper to trim leading and trailing whitespace.
trim :: String -> String
trim = f . f
  where f = reverse . dropWhile isSpace

-- | Validate that a string field is not empty or whitespace-only.
validateNonEmpty :: String -> String -> Either String String
validateNonEmpty fieldName value =
  let trimmed = trim value
  in if null trimmed
       then Left (fieldName ++ " cannot be empty.")
       else Right trimmed

-- | Validate phone number format (7 to 15 digits, allowing +, -, spaces, ()).
validatePhone :: String -> Either String String
validatePhone value = do
  trimmed <- validateNonEmpty "Phone number" value
  let isValidChar c = isDigit c || c `elem` ("+ -()" :: String)
  if not (all isValidChar trimmed)
    then Left ("'" ++ value ++ "' is not a valid phone number.")
    else
      let digits = filter isDigit trimmed
      in if length digits < 7 || length digits > 15
           then Left "Phone number must contain between 7 and 15 digits."
           else Right trimmed

-- | Validate standard email address format (user@domain.tld).
validateEmail :: String -> Either String String
validateEmail value = do
  trimmed <- validateNonEmpty "Email address" value
  let validChar c = isAlphaNum c || c `elem` ("@._+-%" :: String)
  if not (all validChar trimmed)
    then Left ("'" ++ value ++ "' is not a valid email address.")
    else case break (== '@') trimmed of
      (user, '@' : host)
        | not (null user)
            && not (null host)
            && '.' `elem` host
            && not ("." `isPrefixOf` host)
            && not ("." `isSuffixOf` host) ->
            Right trimmed
      _ -> Left ("'" ++ value ++ "' is not a valid email address.")

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
