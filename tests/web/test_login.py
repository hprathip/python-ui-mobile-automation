import pytest

from playwright.sync_api import expect

from data.users import STANDARD, LOCKED, PROBLEM, PERFORMANCE_GLITCH

@pytest.mark.smoke
@pytest.mark.parametrize(
    "user",
    [
        pytest.param(STANDARD, id="standard"),
        pytest.param(PROBLEM, id="problem"),
        pytest.param(PERFORMANCE_GLITCH, id="performance_glitch"),
    ],
)
def test_valid_users_reach_inventory(login_page, user):
    inventory = login_page.login(user)
    expect(inventory.title).to_have_text("Products")


@pytest.mark.smoke
def test_locked_user_sees_error(login_page):
    login_page.login(LOCKED)
    expect(login_page.error).to_contain_text("locked out")
