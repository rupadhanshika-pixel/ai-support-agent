
def classify_customer_issue(issue: str) -> str:
    """Classify a customer support issue using simple keyword rules."""

    text = issue.lower()

    billing_keywords = [
        "charged", "payment", "refund", "bill", "subscription"
    ]
    account_keywords = [
        "login", "password", "account", "sign in", "locked"
    ]
    technical_keywords = [
        "error", "bug", "not working", "crash", "slow", "failed"
    ]

    if any(word in text for word in billing_keywords):
        return "Billing"

    if any(word in text for word in account_keywords):
        return "Account"

    if any(word in text for word in technical_keywords):
        return "Technical"

    return "General"
