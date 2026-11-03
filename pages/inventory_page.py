from playwright.sync_api import Page

from pages.base_page import BasePage


class InventoryPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.title = page.get_by_test_id("title")
        self.cart_badge = page.get_by_test_id("shopping-cart-badge")
        self.sort_dropdown = page.get_by_test_id("product-sort-container")
        self.inventory_item = page.get_by_test_id("inventory-item")

    def add_to_cart(self, product_name):
        self.inventory_item.filter(has_text=product_name).get_by_role(
            "button", name="Add to cart"
        ).click()
        return self

    def sort_by(self, label):
        self.sort_dropdown.select_option(label=label)
        return self

    def prices(self):
        return [
            float(p.strip("$"))
            for p in self.page.get_by_test_id(
                "inventory-item-price"
            ).all_text_contents()
        ]
