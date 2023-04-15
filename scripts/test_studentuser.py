from playwright.sync_api import Playwright, sync_playwright, expect

# if test does not time out or fail, everything is working okay


def test_student_workflow() -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("http://localhost:3000/")
        page.get_by_role("link", name="Start").click()
        # expect(page).not.toHaveURL(/.*stats/)
        page.get_by_placeholder("Enter your username").click()
        page.get_by_placeholder("Enter your username").fill("Alejandra")
        page.get_by_placeholder("Enter your username").press("Tab")
        page.get_by_placeholder("Enter your username").click()
        page.get_by_placeholder("Enter your username").fill("AlejandraLeopold")
        page.get_by_placeholder("Enter your username").press("Tab")
        page.get_by_placeholder("Enter your password").click()
        page.get_by_placeholder("Enter your password").fill("1nap.vale.Musty")
        page.get_by_role("button", name="Login").click()
        page.get_by_role(
            "link", name="CS158_2023_SUM: Mathematical Algorithms in C"
        ).click()
        page.get_by_role("link", name="CS158_W1_L1").click()
        page.get_by_role("button", name="Ping").click()
        page.get_by_role("link", name="← Back to Module").click()
        page.get_by_role("link", name="← Home").click()
        page.get_by_role("button", name="Log Out").click()

        # ---------------------
        context.close()
        browser.close()
