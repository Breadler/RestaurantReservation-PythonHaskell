# Module: Customer Management

**Owner:** Member 2
**Status:** Not started

Covers Report.md sections 4.2/4.3 (Implementation), 5.2 (Test Cases), and the Customer-specific parts of 6.1 (Comparison). See [docs/design/project-structure.md](../design/project-structure.md) for the shared architecture and diagrams.

## Functionality Checklist
- [ ] Add customer
- [ ] View customer
- [ ] Update customer
- [ ] Delete customer
- [ ] Customer validation (name, phone, email)

Files: `python/customer.py` · `haskell/Types.hs` (Customer), `haskell/Customer.hs`

---

## 1. Module Design
### Python (OOP)
[Describe the `Customer` class and `CustomerManager` class: attributes, methods, how state is stored.]

### Haskell (FP)
[Describe the `Customer` data type and the pure functions in `Customer.hs`: signatures, how updates return new values instead of mutating.]

## 2. Implementation
### Python
[Explain `add()`, `view()`, `update()`, `delete()` on `CustomerManager`. Include key code extracts.]

### Haskell
[Explain `addCustomer`, `viewCustomer`, `updateCustomer`, `deleteCustomer`. Include key code extracts and type signatures.]

## 3. Code Explanation
[Walk through non-obvious logic, e.g. how customer IDs are generated, how deletion interacts with existing reservations.]

## 4. Test Cases

| Test ID | Test Description | Input | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|
| CUST-01 | Add valid customer | | | | |
| CUST-02 | View existing customer | | | | |
| CUST-03 | Update customer contact info | | | | |
| CUST-04 | Delete customer | | | | |
| CUST-05 | Reject customer with missing name | | | | |
| CUST-06 | Reject customer with invalid phone/email | | | | |

## 5. Testing Results
[Summarize pass/fail outcomes once testing is complete.]

## 6. Challenges Encountered
[Note any difficulties, e.g. validating email/phone formats, handling deletes of customers with active reservations.]

## 7. Module-Specific Discussion (Python vs Haskell)
[Compare how each paradigm handled customer state and validation.]
