import re
from playwright.sync_api import Playwright, sync_playwright, expect


def test_instructor_workflow() -> None:
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

        # navigate to module CS158
        page.get_by_role(
            "link", name="CS158_2023_SUM: Mathematical Algorithms in C"
        ).click()

        # navigate to lecture 1 for week 2
        page.get_by_role("link", name="Week 2, Lecture 1").click()

        # reset temp
        page.get_by_role("button", name="Reset Temp").click()

        # navigate to stats page
        page.get_by_role("listitem").filter(has_text="Stats").click()

        # choose a module
        page.get_by_role("combobox", name="Module selection").select_option(
            "CS155_2023_SUM"
        )

        # choose a lecture
        page.get_by_role("combobox", name="Lecture selection").select_option(
            "CS155_W1_L2_2023_SUM"
        )

        # fv check here for graph - this could be wrong
        expect(
            page.locator(
                ".container > div:nth-child(1) > div:nth-child(2) > div:nth-child(3) > div:nth-child(2)"
            )
        ).to_be_visible()

        # navigate to admin page and log in
        page.get_by_role("link", name="Admin").click()
        page.get_by_label("Username:").click()
        page.get_by_label("Username:").fill("TaliaSinegold")
        page.get_by_label("Password:").click()
        page.get_by_label("Password:").fill("ruminant.3Dethrone")
        page.get_by_role("button", name="Log in").click()

        # navigate to admin view of lectures
        page.get_by_role("link", name="Lectures").click()

        # select lecture to edit
        page.get_by_role(
            "row",
            name="Mathematical Algorithms in C CS158_W1_L1_2023_SUM Week 1, Lecture 1 Intro July 10, 2023",
        ).get_by_role("link", name="Mathematical Algorithms in C").click()
        page.get_by_label("Lecture description:").click()
        page.get_by_label("Lecture description:").fill("Intro and necessary paperwork")
        page.get_by_role("button", name="Save", exact=True).click()

        # fv check if working
        locator = page.locator(
            "#result_list > tbody:nth-child(2) > tr:nth-child(35) > td:nth-child(5)"
        )
        expect(locator).to_contain_text("necessary")

        # log out
        page.get_by_role("button", name="Log out").click()

        # ---------------------
        context.close()
        browser.close()
