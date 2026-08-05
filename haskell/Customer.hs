module Customer
  ( addCustomer
  , viewCustomer
  , updateCustomer
  , deleteCustomer
  ) where

import Types (Customer (..))

-- | Owner: Member 2. See docs/modules/customer.md for design notes,
-- implementation write-up, and test cases this module feeds into.

-- | Add a new customer, returning the updated list.
addCustomer :: Customer -> [Customer] -> [Customer]
addCustomer = error "TODO(Member 2): implement addCustomer"

-- | Find a customer by ID.
viewCustomer :: Int -> [Customer] -> Maybe Customer
viewCustomer = error "TODO(Member 2): implement viewCustomer"

-- | Apply an update function to the customer with the given ID, returning
-- the updated list.
updateCustomer :: Int -> (Customer -> Customer) -> [Customer] -> [Customer]
updateCustomer = error "TODO(Member 2): implement updateCustomer"

-- | Remove a customer by ID, returning the updated list.
--
-- TODO(Member 2): decide how this interacts with existing reservations for
-- the deleted customer (block delete vs. cascade).
deleteCustomer :: Int -> [Customer] -> [Customer]
deleteCustomer = error "TODO(Member 2): implement deleteCustomer"
