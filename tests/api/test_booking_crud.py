from api.payloads import booking_payload


def test_update_replaces_booking(client, make_booking, auth_token):
    booking_id, _ = make_booking()
    new_payload = booking_payload(firstname="Updated", totalprice=999)

    response = client.update_booking(booking_id, new_payload, auth_token)
    assert response.status_code == 200, f"Update failed: {response.status_code} {response.text}"
    assert response.json() == new_payload
    assert client.get_booking(booking_id).json() == new_payload


def test_partial_update_changes_only_given_fields(client, make_booking, auth_token):
    booking_id, payload = make_booking()
    expected = {**payload, "firstname": "Updated"}

    response = client.partial_update_booking(booking_id, {"firstname": "Updated"}, auth_token)
    assert response.status_code == 200, f"Patch failed: {response.status_code} {response.text}"
    assert response.json() == expected
    assert client.get_booking(booking_id).json() == expected


def test_delete_removes_booking(client, make_booking, auth_token):
    booking_id, _ = make_booking()

    response = client.delete_booking(booking_id, auth_token)
    # QUIRK: DELETE returns 201 Created; 200 or 204 would be standard
    assert response.status_code == 201, f"Delete failed: {response.status_code}"

    assert client.get_booking(booking_id).status_code == 404, "Booking still exists after delete"