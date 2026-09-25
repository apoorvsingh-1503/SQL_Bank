# 🏦 Apoorv Banking System

A console-based command-line banking application built with Python and SQLite. This project allows users to manage accounts, handle secure PIN verifications, perform deposits/withdrawals, and manage beneficiary transfers.

## ✨ Features

* **Account Management:** Create new bank accounts with auto-generated account numbers[cite: 2].
* **Multi-Tier Security:** 
  * Standard PIN (SPIN) for everyday login[cite: 5].
  * Transaction-Withdrawal PIN (TWPIN) for money transfers and withdrawals[cite: 2, 6].
  * High Security PIN (HSPIN) and security questions for sensitive actions and account recovery[cite: 2, 5, 7].
* **Beneficiary Operations:** Add, list, delete, and transfer money safely to approved beneficiaries under custom transfer limits[cite: 4].
* **Transaction Logging:** Automatically logs timestamps, actions (Deposit, Withdrawal, Transfer), and amounts to an SQLite database[cite: 3, 6].
* **Safety Protocol:** Triggers account security blocks and data deletion if too many incorrect authentication attempts are made[cite: 5, 7].

---

## 🛠️ Project Structure

```text
SQL_Bank/
│
├── Modules/
│   ├── __init__.py          # Makes Modules a python package
│   ├── accounts.py          # Account creation, loading, and balance updates[cite: 2]
│   ├── beneficiary.py       # Beneficiary management and transfers[cite: 4]
│   ├── transaction.py       # Deposit, withdrawal, and transaction logging[cite: 6]
│   └── utils.py             # Database connectivity and security authentication[cite: 7]
```text

Prerequisites
	.Python 3.x installed on your machine.
Installation & Setup
	Clone the repository:git clone [https://github.com/apoorvsingh-1503/SQL_Bank.git](https://github.com/apoorvsingh-1503/SQL_Bank.git)
cd SQL_Bank
	Run the application: python main.py
Security Note
	Local database files (*.sqlite3) are intentionally excluded from version control via .gitignore to prevent sensitive banking records 	or data from being exposed on GitHub.


