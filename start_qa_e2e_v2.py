from playwright.sync_api import Page, sync_playwright
#import time
from dotenv import load_dotenv
import os
import pytest

load_dotenv()

usuario = os.getenv("OKTA_USER")
password = os.getenv("OKTA_PASS")

API_URL = "https://pesto.qa.neo-dev.wbd.com/run/WBS"
responses = {}

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
'''
def handle_route(route):
    request = route.request
    print(f"Intercepted request to: {request.url}")
    try:
        response = route.fetch()
        status = response.status
        print(f"Response status: {status}")
        try:
            response_body = response.json()
            print(f"Response body: {response_body}")
        except:
            print("Response body is not JSON")
        responses[API_URL] = status
    except Exception as e:
        print(f"Error fetching or processing response: {e}")
        responses[API_URL] = 500
    route.continue_()
'''
@pytest.mark.test_api
def test_example(page: Page):
    # Registrar la interceptación antes de que un request pueda ocurrir
    #page.route(API_URL, handle_route)

    page.goto("https://ssoqa.wbd.com/app/tw_syndiqa_1/exk28gvlvd8DQF44y0h8/sso/saml?SAMLRequest=fZHdboJAEIVfhey97C7aQjeCsTVNTWxqlfaiN2aAjRBhF5gF7Ns3YG1t0ng5f%2BebOTOdHYvcamWNmVY%2B4TYjs2CKUOSlmDcmVRtZNRKNdSxyhWIo%2BKSpldCAGQoFhURhYrGdP6%2BEYzNR1troWOfEWi58spNR4rq3HIBxnoA7HjPPIdb7GejYjFhLxEYuFRpQxicOc25GzBtxJ%2BSuYEzwO5u57gex1t%2FS95lKMrW%2Fvkd0akLxFIbr0fplGxJrIdFkCsyATo0pUVCKqCuwuyixY11QKEtquh1%2BqiSrYMepPB4cb9%2FmbeItXh8nk0%2BWev0M7b0g1hxR1r3gg1bYFLLeyrrNYvm2Wf0iKrAHwXhA%2F7AuchQak9IY8jyC%2BEBOLxCDMfWF99dPhvMuJOjJgtKu62x9MDDg%2FrtkSi9AwSn6%2B%2FngCw%3D%3D")
    page.get_by_role("textbox", name="Username").fill(usuario)
    page.get_by_role("textbox", name="Password").fill(password)
    page.get_by_role("button", name="Sign in").click()
    #time.sleep(1)
    #page.wait_for_selector('button:has-text("Select to get a push")', timeout=10000)
    page.get_by_role("link", name="Select to get a push").click()
    page.wait_for_url("https://qa.syndication.wbd.com/syndi", timeout=30000)

    #page.goto("https://qa.syndication.wbd.com/syndi")

    # Disparar la request y esperar a que se capture
    with page.expect_response(API_URL) as resp_info:
        page.get_by_role("button", name="Import Schedules").click()

    resp = resp_info.value
    responses[API_URL] = resp.status
    print(f"Final status code captured: {resp.status}")

@pytest.mark.test_api
def test_api_status_code():
    assert responses.get(API_URL) == 200, f"API {API_URL} returned status code {responses.get(API_URL)}, expected 200"
