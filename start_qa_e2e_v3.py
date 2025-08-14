from playwright.sync_api import Page, sync_playwright
from dotenv import load_dotenv
import os
import pytest

load_dotenv()

usuario = os.getenv("OKTA_USER")
password = os.getenv("OKTA_PASS")

API_URL = "https://pesto.qa.neo-dev.wbd.com/run/WBS"

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

@pytest.mark.test_api
def test_import_schedules(page: Page):
    # Login en Okta
    page.goto("https://ssoqa.wbd.com/app/tw_syndiqa_1/exk28gvlvd8DQF44y0h8/sso/saml?SAMLRequest=fZHdboJAEIVfhey97C7aQjeCsTVNTWxqlfaiN2aAjRBhF5gF7Ns3YG1t0ng5f%2BebOTOdHYvcamWNmVY%2B4TYjs2CKUOSlmDcmVRtZNRKNdSxyhWIo%2BKSpldCAGQoFhURhYrGdP6%2BEYzNR1troWOfEWi58spNR4rq3HIBxnoA7HjPPIdb7GejYjFhLxEYuFRpQxicOc25GzBtxJ%2BSuYEzwO5u57gex1t%2FS95lKMrW%2Fvkd0akLxFIbr0fplGxJrIdFkCsyATo0pUVCKqCuwuyixY11QKEtquh1%2BqiSrYMepPB4cb9%2FmbeItXh8nk0%2BWev0M7b0g1hxR1r3gg1bYFLLeyrrNYvm2Wf0iKrAHwXhA%2F7AuchQak9IY8jyC%2BEBOLxCDMfWF99dPhvMuJOjJgtKu62x9MDDg%2FrtkSi9AwSn6%2B%2FngCw%3D%3D")
    page.get_by_role("textbox", name="Username").fill(usuario)
    page.get_by_role("textbox", name="Password").fill(password)
    page.get_by_role("button", name="Sign in").click()
    
    # Selección de push
    page.get_by_role("link", name="Select to get a push").click()
    page.wait_for_url("https://qa.syndication.wbd.com/syndi", timeout=30000)

    # Disparar la request de Import Schedules y capturar respuesta
    with page.expect_response(API_URL) as resp_info:
        page.get_by_role("button", name="Import Schedules").click()

    resp = resp_info.value
    assert resp.status == 200, f"API {API_URL} returned status code {resp.status}, expected 200"
    print(f"Final status code captured: {resp.status}")
