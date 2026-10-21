# AI Customer Support Ticket Assistant

An AI-powered customer support application built with Python, Google ADK, Gemini, and SQLite.

## Features

- Customer issue classification: Billing, Account, Technical, and General
- Automatic support ticket creation
- SQLite database integration
- Duplicate ticket prevention for exact matching issues
- Ticket status management: Open, In Progress, and Closed
- View saved support tickets
- Automated database tests

## Tech Stack

- Python
- Google Agent Development Kit (ADK)
- Google Gemini API
- SQLite
- Python `unittest`

## Project Structure

```text
ai-support-agent/
├── customer_support_agent/
│   ├── __init__.py
│   ├── agent.py
│   ├── database.py
│   └── support_tickets.db
├── test_database.py
├── test_duplicate_ticket.py
├── test_tickets.py
├── .env
├── .gitignore
└── README.md
```

## Setup

1. Create and activate a Python virtual environment.
2. Install Google ADK with `python -m pip install google-adk`.
3. Configure your Gemini API key in the `.env` file.
4. Start the agent with `adk run customer_support_agent`.

## Run Tests

```powershell
python test_database.py
python test_duplicate_ticket.py
```

## Security

Never commit API keys or `.env` files to GitHub. Keep customer data and database files private.

## Current Limitations

- Duplicate detection matches the exact customer issue text and category.
- Email notifications and real billing-system integration are not implemented.
- Gemini API usage depends on the project's available quota.
