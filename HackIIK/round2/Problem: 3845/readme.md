# Merkle Root Calculation

## Problem Statement
A blockchain stores transactions in a block. Each block contains a **Merkle root**, a hash value representing all the transactions in that block. The Merkle root is computed recursively by hashing pairs of transactions until only one hash remains.

You are given a list of transactions (represented as strings) and are required to compute the Merkle root for multiple test cases. The hash function to use is **SHA-256**.

### Steps to Compute the Merkle Root
1. **Transaction Hashing**:  
   Each transaction is represented as a string. Compute the **SHA-256** hash of each transaction. SHA-256 is a cryptographic hash function that outputs a 256-bit value, typically represented as a 64-character hexadecimal string.

2. **Pairing Transactions**:  
   Pair the transactions for hashing. If the number of transactions is odd, duplicate the last transaction to make the number even before calculating the Merkle root.

3. **Recursive Hashing**:  
   Hash each pair recursively. Continue the process with the newly computed hashes until only one hash remains. This final hash is the **Merkle root**.

---

## Input Format
The input consists of multiple test cases:
- The first line contains an integer `T` (1 ≤ T ≤ 10), the number of test cases.
- For each test case:
  - The first line contains an integer `N` (1 ≤ N ≤ 100), the number of transactions.
  - The next `N` lines each contain a string `S` (1 ≤ length(S) ≤ 100), representing a transaction.

---

## Output Format
For each test case, output a single line containing the **Merkle root** for the given transactions.

---

## Constraints
1. Transactions are provided as strings.
2. Use the **SHA-256** hash function for computation.
3. If there’s only one transaction in a test case, the Merkle root is simply the SHA-256 hash of that transaction.

---

## Example

### Input
```plaintext
1
1
0x3a6d79e019b10e459d2624f38f24c5ead4db463bc544fec1c53aef85c4f85774
2
3
0x3a6d79e019b10e459d2624f38f24c5ead4db463bc544fec1c53aef85c4f85774
0x169c7efe0b04a3a0bd7a34f966f40a4ef7e087c76b88d4c93c84622253971be7
0x0815794b25543b2d7d5e575d3b441e7c79370a2577023894fd1bf81251371a5a
```

### Expected Output
```plaintext
aa17c79e02cbd20473e0e26e1cd110242a29d8e4a43d1c6b07a6b2037566aa54
1ca2374bfe088e2653104271975d0e5b4c4571ea82f44eb91dcb996d4c9d3eab
```

---

## Example Table

| Test Case | Transactions | Expected Output                                      | Actual Output                                      |
|-----------|--------------|-----------------------------------------------------|---------------------------------------------------|
| 1         | 1            | `aa17c79e02cbd20473e0e26e1cd110242a29d8e4a43d1c6b07a6b2037566aa54` | `aa17c79e02cbd20473e0e26e1cd110242a29d8e4a43d1c6b07a6b2037566aa54` |
| 2         | 3            | `1ca2374bfe088e2653104271975d0e5b4c4571ea82f44eb91dcb996d4c9d3eab` | `1ca2374bfe088e2653104271975d0e5b4c4571ea82f44eb91dcb996d4c9d3eab` |

--- 
