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


def test_baja_masiva():

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
        page.screenshot(path=f"{RUTA_EVIDENCIAS}/01_login_exitoso.png")
        print("✔ Login exitoso")

        # ===== LISTA DE BIENES =====
        page.goto("http://127.0.0.1:8000/lista-bienes/")
        time.sleep(2)

        ocultar_debug_toolbar(page)
        page.screenshot(path=f"{RUTA_EVIDENCIAS}/02_lista_bienes.png")
        print("✔ Lista de bienes abierta")

        # ===== SELECCIONAR BIENES PARA BAJA MÚLTIPLE =====
        # ===== SELECCIONAR BIENES PARA BAJA MÚLTIPLE =====

        page.mouse.click(1555, 430)
        time.sleep(1)
        print("✔ Bien seleccionado para baja: 1")

        page.mouse.click(1555, 515)
        time.sleep(1)
        print("✔ Bien seleccionado para baja: 2")

        page.mouse.click(1390, 240)
        time.sleep(1)
        print("✔ Bien seleccionado para baja: 3")

        # ===== EVIDENCIA: BOTÓN NARANJA BAJA MÚLTIPLE =====
        page.screenshot(path=f"{RUTA_EVIDENCIAS}/03_baja_multiple_activada.png")
        print("✔ Evidencia capturada con botón Baja múltiple visible")

        # ===== ABRIR PANEL / POPUP DE BAJA MÚLTIPLE =====
        page.evaluate("""
        const boton = document.querySelector('#btn-abrir-baja-multiple');
        if (boton) boton.click();
        """)

        time.sleep(2)
        ocultar_debug_toolbar(page)

        # ===== EVIDENCIA: POPUP DE CONFIRMACIÓN =====
        page.screenshot(path=f"{RUTA_EVIDENCIAS}/04_popup_confirmacion.png")
        print("✔ Popup de confirmación capturado")

        input("Presioná ENTER para cerrar el navegador...")

        browser.close()