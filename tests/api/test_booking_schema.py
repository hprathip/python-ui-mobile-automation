from jsonschema import validate

from api.payloads import booking_payload
from api.schemas import BOOKING_SCHEMA, CREATE_BOOKING_RESPONSE_SCHEMA


def test_get_booking_matches_schema(client, make_booking):
    booking_id, _ = make_booking()

    response = client.get_booking(booking_id)
    assert response.status_code == 200, f"Get failed: {response.status_code}"
    validate(instance=response.json(), schema=BOOKING_SCHEMA)


def test_create_response_matches_schema(client, auth_token):
    response = client.create_booking(booking_payload())
    assert response.status_code == 200, f"Create failed: {response.status_code}"
    body = response.json()

    try:
        validate(instance=body, schema=CREATE_BOOKING_RESPONSE_SCHEMA)
    finally:                                         # manual cleanup: no factory here
        if "bookingid" in body:
            client.delete_booking(body["bookingid"], auth_token)