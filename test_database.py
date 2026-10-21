
# import unittest
# import tempfile
# import sqlite3
# from pathlib import Path


# class TicketDatabaseTests(unittest.TestCase):

#     def test_ticket_creation_and_duplicate_detection(self):
#         with tempfile.TemporaryDirectory() as temp_dir:
#             db_path = Path(temp_dir) / "test_tickets.db"

#             with sqlite3.connect(db_path) as connection:
#                 connection.execute("""
#                     CREATE TABLE tickets (
#                         id INTEGER PRIMARY KEY AUTOINCREMENT,
#                         customer_issue TEXT NOT NULL,
#                         category TEXT NOT NULL,
#                         status TEXT DEFAULT 'Open'
#                     )
#                 """)

#                 issue = "I was charged twice"
#                 category = "Billing"

#                 connection.execute(
#                     "INSERT INTO tickets (customer_issue, category) VALUES (?, ?)",
#                     (issue, category)
#                 )

#                 connection.commit()

#                 existing = connection.execute(
#                     "SELECT id FROM tickets WHERE customer_issue = ? AND category = ?",
#                     (issue, category)
#                 ).fetchone()

#                 self.assertIsNotNone(existing)
#                 self.assertEqual(existing[0], 1)

#     def test_ticket_status_default(self):
#         with tempfile.TemporaryDirectory() as temp_dir:
#             db_path = Path(temp_dir) / "test_tickets.db"

#             with sqlite3.connect(db_path) as connection:
#                 connection.execute("""
#                     CREATE TABLE tickets (
#                         id INTEGER PRIMARY KEY AUTOINCREMENT,
#                         customer_issue TEXT NOT NULL,
#                         category TEXT NOT NULL,
#                         status TEXT DEFAULT 'Open'
#                     )
#                 """)

#                 connection.execute(
#                     "INSERT INTO tickets (customer_issue, category) VALUES (?, ?)",
#                     ("Cannot log in", "Account")
#                 )

#                 status = connection.execute(
#                     "SELECT status FROM tickets WHERE id = 1"
#                 ).fetchone()[0]

#                 self.assertEqual(status, "Open")


# if __name__ == "__main__":
#     unittest.main()



import unittest
import sqlite3
import tempfile
import shutil
from pathlib import Path
from customer_support_agent.database import create_database, save_ticket


class TicketDatabaseTests(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = Path(self.temp_dir) / "test_tickets.db"

        connection = sqlite3.connect(self.db_path)
        connection.execute("""
            CREATE TABLE tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_issue TEXT NOT NULL,
                category TEXT NOT NULL,
                status TEXT DEFAULT 'Open'
            )
        """)
        connection.commit()
        connection.close()

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_ticket_creation(self):
        connection = sqlite3.connect(self.db_path)

        connection.execute(
            "INSERT INTO tickets (customer_issue, category) VALUES (?, ?)",
            ("I was charged twice", "Billing")
        )
        connection.commit()

        result = connection.execute(
            "SELECT id FROM tickets WHERE customer_issue = ? AND category = ?",
            ("I was charged twice", "Billing")
        ).fetchone()

        connection.close()

        self.assertIsNotNone(result)
        self.assertEqual(result[0], 1)

    def test_ticket_status_default(self):
        connection = sqlite3.connect(self.db_path)

        connection.execute(
            "INSERT INTO tickets (customer_issue, category) VALUES (?, ?)",
            ("Cannot log in", "Account")
        )
        connection.commit()

        result = connection.execute(
            "SELECT status FROM tickets WHERE id = 1"
        ).fetchone()

        connection.close()

        self.assertEqual(result[0], "Open")


if __name__ == "__main__":
    unittest.main()
