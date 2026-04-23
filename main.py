import sqlite3

# Connect to database (creates file if it doesn't exist)
conn = sqlite3.connect("banking_app.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    balance REAL
)
""")

conn.commit()

# -----------------
# FUNCTIONS
# -----------------

def create_account():
    name = input("Enter your name: ")

    try:
        balance = float(input("Enter balance: "))
    except ValueError:
        print("Invalid balance\n")
        return

    if balance < 0:
        print("Balance cannot be negative\n")
        return

    cursor.execute(
        "INSERT INTO accounts (name, balance) VALUES (?, ?)",
        (name, balance)
    )
    conn.commit()
    print("Account Created\n")


def view_accounts():
    cursor.execute("SELECT id, name, balance FROM accounts")
    rows = cursor.fetchall()

    print("\n--- ACCOUNTS ---")
    if not rows:
        print("No accounts found\n")
        return

    for row in rows:
        print(f"ID: {row[0]} | Name: {row[1]} | Balance: ${row[2]}")

    print()


def deposit():
    view_accounts()

    try:
        acc_id = int(input("Enter Account ID: "))
    except ValueError:
        print("Invalid input (numbers only)\n")
        return

    # CHECK ACCOUNT FIRST
    cursor.execute("SELECT balance FROM accounts WHERE id = ?", (acc_id,))
    result = cursor.fetchone()

    if not result:
        print("Invalid account ID\n")
        return

    # ONLY ASK FOR AMOUNT IF ID IS VALID
    try:
        amount = float(input("Deposit amount: "))
    except ValueError:
        print("Invalid amount (numbers only)\n")
        return

    if amount <= 0:
        print("Invalid amount\n")
        return

    cursor.execute(
        "UPDATE accounts SET balance = balance + ? WHERE id = ?",
        (amount, acc_id)
    )
    conn.commit()

    print("Deposit successful!\n")
def withdraw():
    view_accounts()

    try:
        acc_id = int(input("Enter Account ID: "))
        amount = float(input("Withdraw amount: "))
    except ValueError:
        print("Invalid input (numbers only)\n")
        return

    if amount <= 0:
        print("Invalid amount\n")
        return

    # CHECK FIRST
    cursor.execute("SELECT balance FROM accounts WHERE id = ?", (acc_id,))
    result = cursor.fetchone()

    if not result:
        print("Invalid account ID\n")
        return

    if amount > result[0]:
        print("Not enough balance!\n")
        return

    cursor.execute(
        "UPDATE accounts SET balance = balance - ? WHERE id = ?",
        (amount, acc_id)
    )
    conn.commit()

    print("Withdrawal successful!\n")


# -----------------
# MENU SYSTEM
# -----------------

while True:
    print("=== BANK MENU ===")
    print("1. Create Account")
    print("2. View Accounts")
    print("3. Deposit")
    print("4. Withdraw")
    print("5. Exit")

    choice = input("Choose option: ")

    if choice == "1":
        create_account()

    elif choice == "2":
        view_accounts()

    elif choice == "3":
        deposit()

    elif choice == "4":
        withdraw()

    elif choice == "5":
        print("Goodbye!")
        break

    else:
        print("Invalid option\n")

# CLOSE DATABASE
conn.close()