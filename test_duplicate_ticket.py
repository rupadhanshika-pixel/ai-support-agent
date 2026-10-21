
import sqlite3
import tempfile
import shutil
from pathlib import Path

from customer_support_agent import database


temp_dir = tempfile.mkdtemp()
test_db = Path(temp_dir) / "test_tickets.db"
original_path = database.DB_PATH

try:
    database.DB_PATH = test_db

    database.create_database()

    first = database.save_ticket(
        "I was charged twice for my subscription.",
        "Billing"
    )

    second = database.save_ticket(
        "I was charged twice for my subscription.",
        "Billing"
    )

    print("First result:", first)
    print("Second result:", second)

    connection = sqlite3.connect(test_db)
    count = connection.execute(
        "SELECT COUNT(*) FROM tickets"
    ).fetchone()[0]
    connection.close()

    print("Total tickets:", count)

    assert first["created"] is True
    assert second["created"] is False
    assert first["ticket_id"] == second["ticket_id"]
    assert count == 1

    print("PASS: Duplicate ticket prevention works!")

finally:
    database.DB_PATH = original_path
    shutil.rmtree(temp_dir, ignore_errors=True)
