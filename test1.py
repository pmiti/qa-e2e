import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.google.com/")
    page.get_by_role("dialog").locator("div").filter(has_text="Accede a GoogleControla los").nth(1).click()
    page.get_by_role("combobox", name="Buscar").click()
    page.get_by_role("combobox", name="Buscar").dblclick()
    page.get_by_role("combobox", name="Buscar").fill("hola")
    page.get_by_role("combobox", name="Buscar").press("ArrowDown")
    page.get_by_text("hola google").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
