from playwright.sync_api import Page, expect

from data.users import STANDARD

def test_inventory_works_without_images(page: Page, login_page):
    blocked = []
    def block_images(route):
        if route.request.resource_type=="image":
            blocked.append(route.request.url)
            route.abort()
        else:
            route.continue_()

    page.route("**/*", block_images)

    inventory = login_page.login(STANDARD)
    expect(inventory.title).to_have_text("Products")

    assert len(blocked) > 0, f"Expected the image requests to be blocked, but total blocked are: {blocked}"



    