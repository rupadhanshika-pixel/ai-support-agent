
from customer_support_agent.database import (
    create_database,
    save_ticket,
    update_ticket_status,
    get_all_tickets,
)

create_database()

# Create a test ticket
result = save_ticket(
    "Test issue for status update",
    "Technical",
)

ticket_id = result["ticket_id"]

# Update ticket status
updated = update_ticket_status(ticket_id, "In Progress")
assert updated is True, "Ticket status update failed!"

# Verify the status
tickets = get_all_tickets()
ticket = next(row for row in tickets if row[0] == ticket_id)

assert ticket[3] == "In Progress", "Status was not saved!"

print("PASS: Ticket status updated successfully!")
print("Ticket ID:", ticket_id)
print("Status:", ticket[3])
