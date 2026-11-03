import pytest

from playwright.sync_api import Page, expect

from config.urls import FRUITS_DEMO, FRUITS_ENDPOINT


def test_api_success_response(page: Page):
    with page.expect_response(FRUITS_ENDPOINT) as response_info:
        page.goto(FRUITS_DEMO)

    response = response_info.value
    assert response.status == 200, f"The API call for the page: {FRUITS_DEMO} failed"

    fruits = response.json()
    assert (
        isinstance(fruits, list) and len(fruits) > 0
    ), f"Expected a non-empty list, got: {fruits}"
    print(fruits[0])


def test_fruits_api_response_show_mocked_fruits_data(page: Page):
    calls = []

    def mock_fruits(route):
        calls.append(route.request.url)
        route.fulfill(
            json=[
                {"name": "Harika's Mango", "id": 1},
                {"name": "Priya's Orange", "id": 2},
            ]
        )

    page.route(FRUITS_ENDPOINT, mock_fruits)

    with page.expect_response(FRUITS_ENDPOINT):
        page.goto(FRUITS_DEMO)

    expect(page.get_by_role("listitem")).to_have_count(2)
    expect(page.get_by_text("Harika's Mango")).to_be_visible()
    expect(page.get_by_text("Priya's Orange")).to_be_visible()

    expect(page.get_by_text("Banana")).not_to_be_visible()
    assert len(calls) == 1, f"Expected the mock to be hit once, got: {calls}"


@pytest.mark.xfail(strict=True, reason="BUG: infinite 'Loading...' when fruits API returns 500 - no error state")
def test_fruits_page_shows_error_when_api_fails(page: Page):

    def mock_internal_server_error(route):
        route.fulfill(status=500, body="Internal Server Error")

    page.route(FRUITS_ENDPOINT, mock_internal_server_error)

    with page.expect_response(FRUITS_ENDPOINT) as response_info:
        page.goto(FRUITS_DEMO)

    response = response_info.value

    assert response.status == 500, "The internal server error couldn't be mocked"
    expect(page.get_by_role("heading", name="Render a List of Fruits")).to_be_visible()
    expect(page.get_by_text("Loading...")).not_to_be_visible()


def test_modified_actual_api_response_in_ui(page: Page):

    def append_own_data(route):
        response = route.fetch()
        fruits = response.json()
        fruits.append(
            {"name": "Harika's Mango", "id": max(f["id"] for f in fruits) + 1}
        )
        route.fulfill(response=response, json=fruits)

    page.route(FRUITS_ENDPOINT, append_own_data)

    with page.expect_response(FRUITS_ENDPOINT):
        page.goto(FRUITS_DEMO)

    expect(page.get_by_text("Tomato")).to_be_visible()

    expect(page.get_by_text("Harika's Mango")).to_be_visible()
