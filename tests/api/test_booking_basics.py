import pytest

BAD_CREDENTIALS = [
    pytest.param("not_a_user", "password123", id="wrong_username"),
    pytest.param("admin", "wrong-password", id="wrong_password"),
]


def test_ping_returns_created(client):
    response = client.ping()
    # QUIRK: /ping returns 201 Created for a health check; 200 OK would be standard
    assert response.status_code == 201, f"Health check failed: {response.status_code}"


def test_list_bookings_returns_ids(client):
    response = client.get_booking_ids()
    assert response.status_code == 200, f"List failed: {response.status_code}"

    bookings = response.json()
    assert isinstance(bookings, list) and bookings, f"Expected a non-empty list, got: {bookings}"
    assert all("bookingid" in b for b in bookings), f"Items missing bookingid: {bookings}"


def test_create_booking_can_be_read_back(client, make_booking):
    booking_id, payload = make_booking()

    response = client.get_booking(booking_id)
    assert response.status_code == 200, f"Created booking {booking_id} not found"
    assert response.json() == payload


@pytest.mark.parametrize("username, password", BAD_CREDENTIALS)
def test_bad_credentials_issue_no_token(client, username, password):
    response = client.auth(username, password)
    body = response.json()
    assert "token" not in body, f"Token issued for bad credentials: {body}"


@pytest.mark.xfail(strict=True, reason="QUIRK: /auth returns 200 (not 401) for bad credentials")
@pytest.mark.parametrize("username, password", BAD_CREDENTIALS)
def test_bad_credentials_return_401(client, username, password):
    response = client.auth(username, password)
    assert response.status_code == 401, f"Expected 401, got {response.status_code}"