
# from google.adk.agents.llm_agent import Agent

# root_agent = Agent(
#     model='gemini-3.8-flash',
#     name='root_agent',
#     description='An AI assistant that helps customers with support issues.',
#     instruction="""
#     You are an AI Customer Support Assistant.

#     Your responsibilities:
#     1. Understand the customer's problem.
#     2. Classify the issue as Billing, Technical, Account, or General.
#     3. Respond politely and professionally.
#     4. Ask relevant questions if more information is needed.
#     5. Never claim that a refund or account change has been completed.
#        Explain that a human support team may need to verify the request.
#     6. Give clear, simple, step-by-step troubleshooting guidance.

#     Always be empathetic, helpful, and concise.
#     """
# )


#line comment:select mutileple and ctrl+/


# from google.adk.agents.llm_agent import Agent


# def classify_customer_issue(issue: str) -> dict:
#     """Classify a customer support issue into a category."""

#     text = issue.lower()

#     if any(word in text for word in ["charged twice", "payment", "billing", "refund", "invoice"]):
#         category = "Billing"
#     elif any(word in text for word in ["login", "password", "account", "sign in"]):
#         category = "Account"
#     elif any(word in text for word in ["error", "crash", "not working", "bug", "app"]):
#         category = "Technical"
#     else:
#         category = "General"

#     return {
#         "category": category,
#         "customer_issue": issue
#     }


# root_agent = Agent(
#     model="gemini-3.8-flash",
#     name="root_agent",
#     description="An AI customer support assistant.",
#     instruction="""
#     Help customers politely and professionally.
#     When a customer describes a problem, use the
#     classify_customer_issue tool to identify its category.
#     Explain the category and suggest appropriate next steps.
#     Never claim that a refund or account change is completed.
#     """,
#     tools=[classify_customer_issue],
# )

from google.adk.agents.llm_agent import Agent
from .database import create_database, save_ticket


# Create database table
create_database()


# Tool 1: Classify customer issue
def classify_customer_issue(issue: str) -> dict:
    """Classify a customer support issue into a category."""

    text = issue.lower()

    if any(word in text for word in [
        "charged twice", "payment", "billing", "refund", "invoice"
    ]):
        category = "Billing"

    elif any(word in text for word in [
        "login", "password", "account", "sign in"
    ]):
        category = "Account"

    elif any(word in text for word in [
        "error", "crash", "not working", "bug", "app"
    ]):
        category = "Technical"

    else:
        category = "General"

    return {
        "category": category,
        "customer_issue": issue
    }


# Tool 2: Save customer complaint
# def create_support_ticket(issue: str, category: str) -> dict:
#     """Save a customer support complaint and generate a ticket ID."""

#     ticket_id = save_ticket(issue, category)

#     return {
#         "ticket_id": ticket_id,
#         "category": category,
#         "status": "Open",
#         "message": "Support ticket created successfully"
#     }

def create_support_ticket(issue: str, category: str) -> dict:
    """Create a support ticket or return an existing matching ticket."""

    result = save_ticket(issue, category)

    if result["created"]:
        message = "New support ticket created successfully."
    else:
        message = "An existing matching support ticket was found."

    return {
        "ticket_id": result["ticket_id"],
        "category": category,
        "status": result["status"],
        "created": result["created"],
        "message": message,
    }



# AI Agent
root_agent = Agent(
    model="gemini-3.8-flash",
    name="root_agent",

    description="An AI customer support assistant.",

    instruction="""
    You are an AI Customer Support Assistant.

    When a customer reports an issue:

    1. Use classify_customer_issue to identify the category.
    2. Use create_support_ticket to save the complaint.
    3. Tell the customer their ticket ID.
    4. Explain the category.
    5. Suggest appropriate next steps.

    Do not create duplicate tickets for the same request.
    Never claim that a refund or account change is completed.
    """,

    tools=[
        classify_customer_issue,
        create_support_ticket
    ],
)
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

session_service = InMemorySessionService()

runner = Runner(
    agent=root_agent,
    app_name="customer_support",
    session_service=session_service,
)