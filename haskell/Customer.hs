module Customer
  ( addCustomer
  , viewCustomer
  , updateCustomer
  , deleteCustomer
  ) where

import Data.List (find)

import Types (Customer (..))

-- | Add a new customer, returning the updated list.
addCustomer :: Customer -> [Customer] -> [Customer]
addCustomer customer customers = customers ++ [customer]

-- | Find a customer by ID.
viewCustomer :: Int -> [Customer] -> Maybe Customer
viewCustomer cid = find ((== cid) . customerId)

-- | Apply an update function to the customer with the given ID, returning
-- the updated list (unchanged if customer ID is not found).
updateCustomer :: Int -> (Customer -> Customer) -> [Customer] -> [Customer]
updateCustomer cid f = map apply
  where
    apply c
      | customerId c == cid = f c
      | otherwise           = c

-- | Remove a customer by ID, returning the updated list.
deleteCustomer :: Int -> [Customer] -> [Customer]
deleteCustomer cid = filter ((/= cid) . customerId)
