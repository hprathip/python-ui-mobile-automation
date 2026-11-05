import uuid

def booking_payload(**overrides) -> dict:
    payload = {
        "firstname": f"Alice-{uuid.uuid4().hex[:6]}",
        "lastname": "Priya",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {"checkin": "2026-12-01", "checkout": "2026-12-05"},
        "additionalneeds": "Breakfast",
    }

    payload.update(overrides)
    return payload