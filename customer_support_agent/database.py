
# import sqlite3


# def create_database():
#     connection = sqlite3.connect("support_tickets.db")

#     cursor = connection.cursor()

#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS tickets (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             customer_issue TEXT NOT NULL,
#             category TEXT NOT NULL,
#             status TEXT DEFAULT 'Open'
#         )
#     """)

#     connection.commit()
#     connection.close()


# def save_ticket(customer_issue, category):
#     connection = sqlite3.connect("support_tickets.db")

#     cursor = connection.cursor()

#     cursor.execute(
#         "INSERT INTO tickets (customer_issue, category) VALUES (?, ?)",
#         (customer_issue, category)
#     )

#     ticket_id = cursor.lastrowid

#     connection.commit()
#     connection.close()

#     return ticket_id

# def save_ticket(customer_issue, category):
#     connection = sqlite3.connect("support_tickets.db")
#     cursor = connection.cursor()

#     cursor.execute(
#         """
#         SELECT id FROM tickets
#         WHERE customer_issue = ? AND category = ?
#         """,
#         (customer_issue, category)
#     )

#     existing_ticket = cursor.fetchone()

#     if existing_ticket:
#         connection.close()
#         return existing_ticket[0]

#     cursor.execute(
#         "INSERT INTO tickets (customer_issue, category) VALUES (?, ?)",
#         (customer_issue, category)
#     )

#     ticket_id = cursor.lastrowid
#     connection.commit()
#     connection.close()

#     return ticket_id


# import sqlite3
# from pathlib import Path

# DB_PATH = Path(__file__).resolve().parent / "support_tickets.db"


# def create_database():
#     with sqlite3.connect(DB_PATH) as connection:
#         connection.execute("""
#             CREATE TABLE IF NOT EXISTS tickets (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 customer_issue TEXT NOT NULL,
#                 category TEXT NOT NULL,
#                 status TEXT DEFAULT 'Open'
#             )
#         """)


# def save_ticket(customer_issue, category):
#     with sqlite3.connect(DB_PATH) as connection:
#         cursor = connection.cursor()

#         cursor.execute(
#             """
#             SELECT id FROM tickets
#             WHERE customer_issue = ? AND category = ?
#             ORDER BY id LIMIT 1
#             """,
#             (customer_issue, category)
#         )

#         existing_ticket = cursor.fetchone()

#         if existing_ticket:
#             return {
#                 "ticket_id": existing_ticket[0],
#                 "created": False,
#                 "status": "Open"
#             }

#         cursor.execute(
#             """
#             INSERT INTO tickets (customer_issue, category)
#             VALUES (?, ?)
#             """,
#             (customer_issue, category)
#         )

#         return {
#             "ticket_id": cursor.lastrowid,
#             "created": True,
#             "status": "Open"
#         }



import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "support_tickets.db"


def create_database():
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_issue TEXT NOT NULL,
                category TEXT NOT NULL,
                status TEXT DEFAULT 'Open'
            )
        """)


def save_ticket(customer_issue, category):
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, status FROM tickets
            WHERE customer_issue = ? AND category = ?
            ORDER BY id LIMIT 1
        """, (customer_issue, category))

        existing_ticket = cursor.fetchone()

        if existing_ticket:
            return {
                "ticket_id": existing_ticket[0],
                "created": False,
                "status": existing_ticket[1]
            }

        cursor.execute("""
            INSERT INTO tickets (customer_issue, category)
            VALUES (?, ?)
        """, (customer_issue, category))

        return {
            "ticket_id": cursor.lastrowid,
            "created": True,
            "status": "Open"
        }
def update_ticket_status(ticket_id, new_status):
    allowed_statuses = ["Open", "In Progress", "Closed"]

    if new_status not in allowed_statuses:
        raise ValueError("Invalid ticket status")

    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()

        cursor.execute(
            "UPDATE tickets SET status = ? WHERE id = ?",
            (new_status, ticket_id)
        )

        return cursor.rowcount > 0

def get_all_tickets():
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, customer_issue, category, status
            FROM tickets
            ORDER BY id
        """)

        return cursor.fetchall()
