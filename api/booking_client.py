import requests


class BookingClient:
    """Wraps the Restful Booker API. Methods return the raw Response; tests decide what's correct."""

    def __init__(self, session: requests.Session, base_url: str, timeout: int = 10):
        self.session = session
        self.base_url = base_url
        self.timeout = timeout

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    @staticmethod
    def _auth_headers(token: str | None) -> dict:
        # No token → send no Cookie header at all (not "token=None")
        return {"Cookie": f"token={token}"} if token else {}

    def ping(self) -> requests.Response:
        return self.session.get(self._url("/ping"), timeout=self.timeout)

    def auth(self, username: str, password: str) -> requests.Response:
        return self.session.post(
            self._url("/auth"),
            json={"username": username, "password": password},
            timeout=self.timeout,
        )

    def get_booking_ids(self) -> requests.Response:
        return self.session.get(self._url("/booking"), timeout=self.timeout)

    def get_booking(self, booking_id: int) -> requests.Response:
        return self.session.get(self._url(f"/booking/{booking_id}"), timeout=self.timeout)

    def create_booking(self, payload: dict) -> requests.Response:
        return self.session.post(self._url("/booking"), json=payload, timeout=self.timeout)

    def update_booking(self, booking_id: int, payload: dict, token: str | None = None) -> requests.Response:
        return self.session.put(
            self._url(f"/booking/{booking_id}"),
            json=payload,
            headers=self._auth_headers(token),
            timeout=self.timeout,
        )

    def partial_update_booking(self, booking_id: int, fields: dict, token: str | None = None) -> requests.Response:
        return self.session.patch(
            self._url(f"/booking/{booking_id}"),
            json=fields,
            headers=self._auth_headers(token),
            timeout=self.timeout,
        )

    def delete_booking(self, booking_id: int, token: str | None = None) -> requests.Response:
        return self.session.delete(
            self._url(f"/booking/{booking_id}"),
            headers=self._auth_headers(token),
            timeout=self.timeout,
        )