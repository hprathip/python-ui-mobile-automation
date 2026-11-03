import pytest

from playwright.sync_api import expect

from data.users import PROBLEM

@pytest.mark.smoke
def test_cart_badge_after_adding_items_to_cart(inventory_page):
    inventory_page.add_to_cart("Sauce Labs Backpack").add_to_cart(
        "Sauce Labs Bike Light"
    )

    expect(inventory_page.cart_badge).to_have_text("2")

@pytest.mark.smoke
def test_items_sort_by_price_low_to_high(inventory_page):
    expected_all_prices = inventory_page.prices()

    actual_prices_after_sorting_ui = inventory_page.sort_by("Price (low to high)").prices()
    assert len(expected_all_prices) == 6, f"Expected 6 products, got {expected_all_prices}"
    assert actual_prices_after_sorting_ui == sorted(expected_all_prices), f"the prices are not sorted from low -> high: {actual_prices_after_sorting_ui}"

@pytest.mark.regression
def test_items_sort_by_price_high_to_low(inventory_page):
    expected_all_prices = inventory_page.prices()

    actual_prices_after_sorting_ui = inventory_page.sort_by("Price (high to low)").prices()
    assert len(expected_all_prices) == 6, f"Expected 6 products, got {expected_all_prices}"
    assert actual_prices_after_sorting_ui == sorted(expected_all_prices, reverse=True), f"the prices are not sorted from high -> low: {actual_prices_after_sorting_ui}"

@pytest.mark.regression
@pytest.mark.xfail(strict=True, reason="BUG: sort has no effect for problem_user")
def test_problem_user_can_sort_by_price(login_page):
    inventory = login_page.login(PROBLEM)
    original = inventory.prices()
    expected = [f"${p:.2f}" for p in sorted(original)]

    inventory.sort_by("Price (low to high)")
    expect(inventory.price_labels).to_have_text(expected, timeout=3_000)