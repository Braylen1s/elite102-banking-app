import unittest
import sqlite3

# connect to SAME database
conn = sqlite3.connect("banking_app.db")
cursor = conn.cursor()


# ---- helper function for tests ----
def is_positive(n):
    return n > 0


class TestBankingApp(unittest.TestCase):

    def test_create_account(self):
        # insert test account
        cursor.execute(
            "INSERT INTO accounts (name, balance) VALUES (?, ?)",
            ("TestUser", 100.0)
        )
        conn.commit()

        # check it exists
        cursor.execute("SELECT balance FROM accounts WHERE name = ?", ("TestUser",))
        result = cursor.fetchone()

        self.assertIsNotNone(result)
        self.assertEqual(result[0], 100.0)
def test_deposit_logic(self):
    # CLEAN OLD TEST DATA FIRST
    cursor.execute("DELETE FROM accounts WHERE name = 'DepositUser'")
    conn.commit()

    # create test account
    cursor.execute(
        "INSERT INTO accounts (name, balance) VALUES (?, ?)",
        ("DepositUser", 50.0)
    )
    conn.commit()

    # get correct id
    cursor.execute("SELECT id FROM accounts WHERE name = ?", ("DepositUser",))
    acc_id = cursor.fetchone()[0]

    # deposit
    cursor.execute(
        "UPDATE accounts SET balance = balance + ? WHERE id = ?",
        (25.0, acc_id)
    )
    conn.commit()

    # check result
    cursor.execute("SELECT balance FROM accounts WHERE id = ?", (acc_id,))
    new_balance = cursor.fetchone()[0]

    self.assertEqual(new_balance, 75.0)
    def test_invalid_account(self):
        # try fake ID
        cursor.execute("SELECT * FROM accounts WHERE id = ?", (999999,))
        result = cursor.fetchone()

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
    conn.close()