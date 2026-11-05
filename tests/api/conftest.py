import pytest
import requests

from api.booking_client import BookingClient
from api.payloads import booking_payload
from config.urls import RESTFUL_BOOKER


@pytest.fixture(scope="session")
def api_session():
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json", "Accept": "application/json"})
    yield session
    session.close()


@pytest.fixture(scope="session")
def client(api_session):
    return BookingClient(api_session, RESTFUL_BOOKER)


@pytest.fixture(scope="session")
def auth_token(client):
    response = client.auth("admin", "password123")
    assert response.status_code == 200, f"Auth failed: {response.text}"
    token = response.json().get("token")
    assert token, f"No token in auth response: {response.json()}"
    return token


@pytest.fixture
def make_booking(client, auth_token):
    """Factory: creates bookings for a test and deletes all of them afterwards."""
    created_ids = []

    def _make(**overrides):
        payload = booking_payload(**overrides)
        response = client.create_booking(payload)
        assert response.status_code == 200, f"Create failed: {response.status_code} {response.text}"
        body = response.json()
        assert body["booking"] == payload, f"Create response doesn't echo the payload: {body}"
        created_ids.append(body["bookingid"])
        return body["bookingid"], payload

    yield _make

    for booking_id in created_ids:
        client.delete_booking(booking_id, auth_token)   # already-deleted ids just return 404, harmless