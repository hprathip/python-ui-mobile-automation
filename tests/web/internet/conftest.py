import pytest

from playwright.sync_api import Page

from config.urls import THE_INTERNET

@pytest.fixture
def open_internet(page: Page):
    def _open(path: str) -> Page:
        page.goto(f"{THE_INTERNET}/{path}")
        return page
    return _open