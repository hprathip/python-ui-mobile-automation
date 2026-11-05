import pytest

from api.payloads import booking_payload

INVALID_TOKENS = [
    pytest.param(None, id="no_token"),
    pytest.param("not-a-real-token", id="invalid_token"),
]


@pytest.mark.parametrize("token", INVALID_TOKENS)
def test_update_refused_without_valid_token(client, make_booking, token):
    booking_id, payload = make_booking()

    response = client.update_booking(booking_id, booking_payload(firstname="Hacker"), token)
    assert response.status_code == 403, f"Expected refusal, got {response.status_code}"
    assert client.get_booking(booking_id).json() == payload, "Refused update still changed the booking"


@pytest.mark.parametrize("token", INVALID_TOKENS)
def test_delete_refused_without_valid_token(client, make_booking, token):
    booking_id, _ = make_booking()

    response = client.delete_booking(booking_id, token)
    assert response.status_code == 403, f"Expected refusal, got {response.status_code}"
    assert client.get_booking(booking_id).status_code == 200, "Refused delete still removed the booking"


def test_get_deleted_booking_returns_404(client, make_booking, auth_token):
    booking_id, _ = make_booking()
    client.delete_booking(booking_id, auth_token)    # an id guaranteed not to exist anymore

    response = client.get_booking(booking_id)
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"


def _create_without_firstname(client, auth_token):
    payload = booking_payload()
    del payload["firstname"]
    response = client.create_booking(payload)
    if response.ok:                                  # created anyway → don't leak it
        client.delete_booking(response.json()["bookingid"], auth_token)
    return response


def test_create_without_required_field_is_rejected(client, auth_token):
    response = _create_without_firstname(client, auth_token)
    assert response.status_code >= 400, f"Invalid booking was accepted: {response.status_code}"


@pytest.mark.xfail(strict=True, reason="QUIRK: missing required field returns 500 (not 400)")
def test_create_without_required_field_returns_400(client, auth_token):
    response = _create_without_firstname(client, auth_token)
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"