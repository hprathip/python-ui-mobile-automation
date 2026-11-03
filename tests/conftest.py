import pytest

from data.users import STANDARD
from pages.login_page import LoginPage

@pytest.fixture(scope="session", autouse=True)
def set_test_id_attribute(playwright):
    playwright.selectors.set_test_id_attribute("data-test")

@pytest.fixture
def login_page(page):
    return LoginPage(page).open()

@pytest.fixture
def inventory_page(login_page):
    return login_page.login(STANDARD)