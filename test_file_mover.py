from playwright.sync_api import Page, sync_playwright
from dotenv import load_dotenv
import os
import pytest
from pathlib import Path
import time

load_dotenv()

usuario = os.getenv("OKTA_USER")
password = os.getenv("OKTA_PASS")

#API_URL = "https://api.para.validar"

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Cambiar a True en CI/CD
        yield browser
        browser.close()

@pytest.fixture(scope="session")
def page(browser):
    page = browser.new_page()
    yield page

@pytest.mark.file_mover_caso1
def test_file_mover_caso1(page: Page):
    # Login en Okta
    page.goto("https://ssodev.wbd.com/app/twdev_clpfilemover_1/exk2080qwj3HLaaVK0h8/sso/saml?SAMLRequest=jZFBb4JAEIX%2FCtk77IIt0o1gbD1oalOj1EMvZlmmSl12KbOgP78Ba2ovpsfJzLxv5r3R%2BFQqp4UaC6Nj4nuMjJMRilJVfNLYvV7BVwNonVOpNPK%2BEZOm1twILJBrUQJyK%2Fl68rLggcd4VRtrpFHEmU9jss380A%2BHoRwEGctzMRwE0ZA4mwsw8Bhx5ogNzDVaoW1MAhbcuyxy%2FbvUj7gf8mDoPYT%2BO3GWP9KPhc4Lvbt9R3YeQj5L06W7fF2nxJkC2kIL26P31lbIKUU0ObTeMcs9aUoqqoraYw7tVqrqo1BQmhbqrU%2FhdAhYxL6On4PZQojNM9tH3TLtTCHOBBHqTvnJaGxKqNdQt4WEt9Xil9Xpub2g1zE1GPearcyu0FQKpTIhD%2BQcBO%2Ftqa8SuP24uBxCkv9hR%2FQKk5yrv%2Bkn3w%3D%3D")

    page.get_by_role("textbox", name="Username").fill(usuario)
    page.get_by_role("button", name="Next").click()
    page.get_by_role("textbox", name="Password").fill(password)
    page.get_by_role("button", name="Verify").click()

    # Selección de push
    page.get_by_role("link", name="Select to get a push").click()
    page.wait_for_url("https://file-mover.dev.neo-dev.wbd.com/", timeout=30000)

    # Upload Files
    file_path = Path(__file__).parent / "resources" / "image.png"
    page.set_input_files("input[type='file']", str(file_path))    

    page.get_by_role("combobox").click()
    page.get_by_role("option", name="Graphic").click()
    page.get_by_role("combobox").filter(has_text="Select Sub Type").click()
    page.get_by_text("Moving").click()
    page.get_by_role("cell", name="prod uat qa dev local").get_by_label("qa").click()
    time.sleep(3)
    #mejorar esta parte, avanzar cuando el boton este habilitado
    page.get_by_role("button", name="Upload 1").click()
    time.sleep(2)

