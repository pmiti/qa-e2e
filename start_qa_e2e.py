from playwright.sync_api import sync_playwright, TimeoutError
from dotenv import load_dotenv
import os

load_dotenv()

usuario = os.getenv("OKTA_USER")
password = os.getenv("OKTA_PASS")

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Funciones para loguear requests y responses
        def log_request(request):
            print(f"➡️ {request.method} {request.url}")
            if request.post_data:
                print(f"   Payload: {request.post_data}")

        def log_response(response):
            print(f"⬅️ {response.status} {response.url}")
            try:
                text = response.text()
                print(f"   Response body: {text[:300]}")  # Primeros 300 caracteres
            except:
                pass

        page.on("request", log_request)
        page.on("response", log_response)

        page.goto("https://qa.syndication.wbd.com")

        print("Esperando redirección a login de Okta...")

        try:
            page.wait_for_url("**ssoqa.wbd.com**", timeout=5000)
            print("Llegó a la URL de login:", page.url)
        except TimeoutError:
            print("Timeout alcanzado. URL actual:", page.url)

        if "ssoqa.wbd.com" in page.url:
            print("Estamos en login Okta, listo para completar formulario")
            page.fill('input[name="identifier"]', usuario)
            page.fill('input[name="credentials.passcode"]', password)
            page.click('input[type="submit"]')

            # Esperar los enlaces "Select" que aparecen en MFA
            try:
                page.wait_for_selector('a:text("Select")', timeout=10000)
                links = page.query_selector_all('a:text("Select")')
                if len(links) > 1:
                    links[1].click()
                    print("Click en segundo enlace 'Select' realizado (MFA)")
                else:
                    print("No se encontró el segundo enlace 'Select'")
            except TimeoutError:
                print("No aparecieron los enlaces 'Select' para MFA")

            # Ahora esperamos que cargue la página principal y aparece botón IMPORT SCHEDULES
            try:
                page.wait_for_selector('button:text("IMPORT SCHEDULES")', timeout=20000)
                print("Botón 'IMPORT SCHEDULES' encontrado, haciendo click...")
                page.click('button:text("IMPORT SCHEDULES")')
            except TimeoutError:
                print("No se encontró el botón 'IMPORT SCHEDULES'")

        else:
            print("No estamos en la pantalla de login Okta")

        input("Presiona Enter para cerrar el navegador...")
        browser.close()

if __name__ == "__main__":
    main()
