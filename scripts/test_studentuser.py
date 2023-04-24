import re
from playwright.sync_api import Playwright, sync_playwright, expect

# if test does not time out or fail, everything is working okay


def test_student_workflow() -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("http://localhost:3000/")

        # check that logging in as a student works
        page.get_by_role("link", name="Start").click()
        page.get_by_placeholder("Enter your username").click()
        page.get_by_placeholder("Enter your username").fill("AlejandraLeopold")
        page.get_by_placeholder("Enter your password").click()
        page.get_by_placeholder("Enter your password").fill("1nap.vale.Musty")
        page.get_by_role("button", name="Login").click()

        # using CSS Selector locator to check for welcome statement
        locator = page.locator(
            "div.col-6:nth-child(2) > div:nth-child(1) > div:nth-child(2) > h3:nth-child(1)"
        )
        expect(locator).to_contain_text(re.compile(r"Alejandra"))

        # check for no stats or admin links on modules page
        expect(page).not_to_have_url(re.compile(".*stats.*"))
        expect(page).not_to_have_url(re.compile(".*admin.*"))

        # navigate to module detail page
        page.get_by_role(
            "link", name="CS158_2023_SUM: Mathematical Algorithms in C"
        ).click()
        # check for no stats or admin links on module detail page
        expect(page).not_to_have_url(re.compile(".*stats.*"))
        expect(page).not_to_have_url(re.compile(".*admin.*"))

        # navigate to lecture page
        page.get_by_role("link", name="Week 1, Lecture 1").click()

        # check that Ping button exists and click it
        page.get_by_role("button", name="Ping").click()

        # check for no stats or admin links on lecture page
        expect(page).not_to_have_url(re.compile(".*stats.*"))
        expect(page).not_to_have_url(re.compile(".*admin.*"))

        page.get_by_role("link", name="← Back to Module").click()

        # check for no stats or admin links on homepage
        expect(page).not_to_have_url(re.compile(".*stats.*"))
        expect(page).not_to_have_url(re.compile(".*admin.*"))
        page.get_by_role("link", name="Home").click()

        # log out
        page.get_by_role("button", name="Log Out").click()

        # ---------------------
        context.close()
        browser.close()
