import re
from playwright.sync_api import Playwright, sync_playwright, expect

# if test does not time out or fail, everything is working okay


def test_student_workflow() -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("http://localhost:3000/")
        page.get_by_role("link", name="Start").click()
        # check that logging in as a student works
        page.get_by_placeholder("Enter your username").click()
        page.get_by_placeholder("Enter your username").fill("Alejandra")
        page.get_by_placeholder("Enter your username").press("Tab")
        page.get_by_placeholder("Enter your username").click()
        page.get_by_placeholder("Enter your username").fill("AlejandraLeopold")
        page.get_by_placeholder("Enter your username").press("Tab")
        page.get_by_placeholder("Enter your password").click()
        page.get_by_placeholder("Enter your password").fill("1nap.vale.Musty")
        page.get_by_role("button", name="Login").click()
        # fv this below is not working
        # locator = page.locator("ul/li[1]/a")
        # expect(locator).to_contain_text(re.compile(r"Mathematical Algorithms in C"))

        # check for no stats or admin links on modules page
        expect(page).not_to_have_url(re.compile(".*stats.*"))
        expect(page).not_to_have_url(re.compile(".*admin.*"))
        page.get_by_role(
            "link", name="CS158_2023_SUM: Mathematical Algorithms in C"
        ).click()
        # check for no stats or admin links on module detail page
        expect(page).not_to_have_url(re.compile(".*stats.*"))
        expect(page).not_to_have_url(re.compile(".*admin.*"))
        page.get_by_role("link", name="CS158_W1_L1").click()
        # check for no stats or admin links on lecture page
        expect(page).not_to_have_url(re.compile(".*stats.*"))
        expect(page).not_to_have_url(re.compile(".*admin.*"))
        # check that Ping button exists and click it
        page.get_by_role("button", name="Ping").click()
        page.get_by_role("link", name="← Back to Module").click()
        # check for no stats or admin links on homepage
        expect(page).not_to_have_url(re.compile(".*stats.*"))
        expect(page).not_to_have_url(re.compile(".*admin.*"))
        page.get_by_role("link", name="← Home").click()
        # log out
        page.get_by_role("button", name="Log Out").click()

        # ---------------------
        context.close()
        browser.close()


# fv - on "unhappy" student path, try clicking ping button twice, look for error message, then try to manually navigate to a wrong module, a wrong lecture, and the stats and admin pages
