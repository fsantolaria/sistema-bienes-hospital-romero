
from playwright.sync_api import sync_playwright
import time


RUTA_EVIDENCIAS = "playwright_test/qa_milagritos/evidencias"


def ocultar_debug_toolbar(page):
    try:
        if page.locator("#djHideToolBarButton").is_visible():
            page.locator("#djHideToolBarButton").click()
            time.sleep(1)
    except:
        pass


def test_notificaciones():

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)

        page = browser.new_page()

        page.set_viewport_size({"width": 1600, "height": 900})

        # ===== LOGIN =====
        page.goto("http://127.0.0.1:8000/login/")

        page.fill('input[name="usuario"]', "mili")
        page.fill('input[type="password"]', "mmmb123456")

        page.click("button")

        time.sleep(2)

        ocultar_debug_toolbar(page)

        page.screenshot(
            path=f"{RUTA_EVIDENCIAS}/05_login_notificaciones.png"
        )

        print("✔ Login exitoso")

        # ===== HOME ADMIN =====
        page.goto("http://127.0.0.1:8000/home_admin/")

        time.sleep(2)

        ocultar_debug_toolbar(page)

        page.screenshot(
            path=f"{RUTA_EVIDENCIAS}/06_home_admin.png"
        )

        print("✔ Home admin abierto")

        # ===== ABRIR PANEL DE NOTIFICACIONES =====
        page.mouse.click(1470, 105)

        time.sleep(2)

        

        print("✔ Panel de notificaciones visualizado")

        input("Presioná ENTER para cerrar el navegador...")

        browser.close()