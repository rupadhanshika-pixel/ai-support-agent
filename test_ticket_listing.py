
from customer_support_agent.database import (
    create_database,
    get_all_tickets,
)

create_database()

tickets = get_all_tickets()

print("Tickets in database:")

for ticket in tickets:
    print(ticket)

print("PASS: Ticket listing completed!")
