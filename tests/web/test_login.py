import pytest

from playwright.sync_api import expect

from data.users import STANDARD, LOCKED, PROBLEM, PERFORMANCE_GLITCH


@pytest.mark.smoke
@pytest.mark.parametrize(
    "user, timeout_ms",
    [
        pytest.param(STANDARD, 5_000, id="standard"),
        pytest.param(PROBLEM, 5_000, id="problem"),
        pytest.param(
            PERFORMANCE_GLITCH, 15_000, id="performance_glitch"
        ),  # known slow login
    ],
)
def test_valid_users_reach_inventory(login_page, user, timeout_ms):
    inventory = login_page.login(user)
    expect(inventory.title).to_have_text("Products", timeout=timeout_ms)


@pytest.mark.smoke
def test_locked_user_sees_error(login_page):
    login_page.login(LOCKED)
    expect(login_page.error).to_contain_text("locked out")
