import re
from playwright.sync_api import Playwright, sync_playwright, expect

# if test does not time out or fail, everything is working okay


def test_bad_student_workflow() -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("http://localhost:3000/")

        # log in incorrectly
        page.get_by_role("link", name="Start").click()
        page.get_by_placeholder("Enter your username").click()
        page.get_by_placeholder("Enter your username").fill("AlejandraLeopold")
        page.get_by_placeholder("Enter your username").press("Tab")
        page.get_by_placeholder("Enter your password").fill("1nap.vale.Musty2")

        # check for invalid entry error text
        locator = page.locator(".user-message")
        expect(locator).to_contain_text(re.compile(r"Invalid login credentials"))

        # log in correctly
        page.get_by_placeholder("Enter your password").fill("1nap.vale.Musty")
        page.get_by_role("button", name="Login").click()

        # navigate to module CS270
        page.get_by_role("link", name="CS270_2023_SUM: Computer Organisation").click()

        # navigate to lecture 1 of week 1
        page.get_by_role("link", name="CS270_W1_L1_2023_SUM").click()

        # submit first ping
        page.get_by_role("button", name="Ping").click()

        # submit second ping immediately
        page.get_by_role("button", name="Ping").click()

        # check for error message too many pings
        locator = page.locator(".user-message")
        expect(locator).to_contain_text(re.compile(r"Too many submissions"))

        # manually navigate to unauthorized module; check that re-route to modules page occurs
        page.goto("http://localhost:3000/modules/CS152_2023_SUM")
        page.goto("http://localhost:3000/modules")

        # manually navigate to unauthorized lecture; check that re-route to modules page occurs
        page.goto("http://localhost:3000/modules/lectures/CS152_W1_L1_2023_SUM")
        page.goto("http://localhost:3000/modules")

        # manually navigate to stats page; check that re-route to modules page occurs
        page.goto("http://localhost:3000/stats")
        page.goto("http://localhost:3000/modules")

        # manually navigate to admin page; check that user is not allowed in
        page.goto("http://localhost:8000/admin/login/?next=/admin/")
        page.get_by_label("Username:").click()
        page.get_by_label("Username:").fill("AlejandraLeopold")
        page.get_by_label("Password:").click()
        page.get_by_label("Password:").fill("1nap.vale.Musty")
        page.get_by_role("button", name="Log in").click()

        # fv check for error message here
        locator = page.locator(".errornote")
        expect(locator).to_contain_text(
            re.compile(
                r"Please enter the correct username and password for a staff account"
            )
        )

        # ---------------------
        context.close()
        browser.close()
