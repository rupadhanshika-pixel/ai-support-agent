
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200


def test_health():
    response = client.get("/health")
    assert response.status_code == 200


def test_get_tickets():
    response = client.get("/tickets")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    


def test_create_ticket():
    response = client.post(
        "/tickets",
        json={
            "customer_issue": "I was charged twice for my subscription.",
            "category": "Billing"
        }
    )

    print("Status code:", response.status_code)
    print("Response:", response.json())

    assert response.status_code == 200


def test_create_ticket_empty_issue():
    response = client.post(
        "/tickets",
        json={
            "customer_issue": "",
            "category": "General"
        }
    )

    assert response.status_code in (400, 422)


def test_update_ticket_status():
    create_response = client.post(
        "/tickets",
        json={
            "customer_issue": "Test issue for status update",
            "category": "General"
        }
    )

    print("Create response:", create_response.json())

    assert create_response.status_code == 200
