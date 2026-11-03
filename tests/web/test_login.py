import re

import pytest

from playwright.sync_api import Page, expect

from data.users import STANDARD, LOCKED

@pytest.mark.smoke
def test_standard_user_can_log_in(page: Page):
    page.goto("/")

    page.get_by_placeholder("Username").fill(STANDARD.username)
    page.get_by_placeholder("Password").fill(STANDARD.password)

    page.get_by_role("button", name="Login").click()

    expect(page).to_have_url(re.compile("inventory"))
    expect(page.get_by_test_id("title")).to_have_text("Products")

@pytest.mark.smoke
def test_locked_user_sees_error(page: Page):
    page.goto("/")
    
    page.get_by_placeholder("Username").fill(LOCKED.username)
    page.get_by_placeholder("Password").fill(LOCKED.password)
    
    page.get_by_role("button", name="Login").click()
    
    expect(page.get_by_test_id("error")).to_contain_text("locked out")
