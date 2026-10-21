# from customer_support_agent.database import create_database, save_ticket

# create_database()

# issue = "I was charged twice for my subscription."
# category = "Billing"

# result = save_ticket(issue, category)

# print("Ticket ID:", result["ticket_id"])
# print("Created:", result["created"])
# print("Category:", category)
# print("Status:", result["status"])



# from customer_support_agent.database import update_ticket_status, DB_PATH
# import sqlite3

# ticket_id = 1
# new_status = "In Progress"

# updated = update_ticket_status(ticket_id, new_status)

# if updated:
#     print("Ticket status updated successfully!")
# else:
#     print("Ticket ID not found.")

# connection = sqlite3.connect(DB_PATH)
# ticket = connection.execute(
#     "SELECT id, customer_issue, category, status FROM tickets WHERE id = ?",
#     (ticket_id,)
# ).fetchone()
# connection.close()

# print("Ticket details:", ticket)


from customer_support_agent.database import get_all_tickets

tickets = get_all_tickets()

if tickets:
    print("\n--- Customer Support Tickets ---")
    for ticket in tickets:
        print(f"""
Ticket ID: {ticket[0]}
Customer Issue: {ticket[1]}
Category: {ticket[2]}
Status: {ticket[3]}
------------------------------
""")
else:
    print("No tickets found.")
