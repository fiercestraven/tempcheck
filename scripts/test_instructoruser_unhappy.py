import re
from playwright.sync_api import Playwright, sync_playwright, expect


def test_bad_instructor_workflow() -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("http://localhost:3000/")

        # log in
        page.get_by_role("link", name="Start").click()
        page.get_by_placeholder("Enter your username").click()
        page.get_by_placeholder("Enter your username").fill("TaliaSinegold")
        page.get_by_placeholder("Enter your password").click()
        page.get_by_placeholder("Enter your password").fill("ruminant.3Dethrone")
        page.get_by_placeholder("Enter your password").press("Enter")

        # manually navigate to unauthorized module; check that re-route to modules page occurs
        page.goto("http://localhost:3000/modules/CS270_2023_SUM")
        page.wait_for_url("http://localhost:3000/modules")
        expect(page).to_have_url("http://localhost:3000/modules")

        # manually navigate to unauthorized lecture; check that re-route to modules page occurs
        page.goto("http://localhost:3000/modules/lectures/CS270_W1_L1_2023_SUM")
        page.wait_for_url("http://localhost:3000/modules")
        expect(page).to_have_url("http://localhost:3000/modules")

        # log out
        page.get_by_role("button", name="Log Out").click()
        page.get_by_role("button", name="Close").click()

        # ---------------------
        context.close()
        browser.close()
