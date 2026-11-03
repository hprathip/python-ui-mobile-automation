from playwright.sync_api import Page

from data.users import User
from pages.base_page import BasePage
from pages.inventory_page import InventoryPage

class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.username = page.get_by_placeholder("Username")
        self.password = page.get_by_placeholder("Password")
        self.login_button = page.get_by_role("button", name="Login")
        self.error = page.get_by_test_id("error")

    def open(self) -> "LoginPage":
        self.page.goto("/")
        return self

    def login(self, user: User) -> InventoryPage:
        self.username.fill(user.username)
        self.password.fill(user.password)
        self.login_button.click()
        return InventoryPage(self.page)