from playwright.sync_api import sync_playwright
import os

RUTA_EVIDENCIA = "QA_Regresion/evidencias/playwright/reportes/"
os.makedirs(RUTA_EVIDENCIA, exist_ok=True)


def ocultar_debug_toolbar(page):
    page.evaluate("""
        const toolbar = document.getElementById('djDebug');
        if (toolbar) {
            toolbar.style.display = 'none';
        }
    """)


def test_reg_pw_004_live_search_reportes():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=250)
        page = browser.new_page(viewport={"width": 1366, "height": 768})

        page.goto("http://127.0.0.1:8000/inicio/", wait_until="domcontentloaded")
        ocultar_debug_toolbar(page)

        try:
            page.get_by_role("button", name="Administrador").click(timeout=2000)
        except Exception:
            print("Botón Administrador no encontrado.")

        page.locator("input[name='usuario'], input[name='username']").fill("admin")
        page.locator("input[type='password']").fill("Hospital@1")
        page.keyboard.press("Enter")
        page.wait_for_timeout(2000)

        page.goto("http://127.0.0.1:8000/reportes/", wait_until="domcontentloaded")
        ocultar_debug_toolbar(page)

        page.screenshot(
            path=RUTA_EVIDENCIA + "REG-PW-004_01_pantalla_reportes.png"
        )

        buscador = page.get_by_placeholder("Descripción, ID...")

        buscador.click()
        buscador.press("v")
        page.wait_for_timeout(1000)

        page.screenshot(
            path=RUTA_EVIDENCIA + "REG-PW-004_02_despues_primera_letra.png"
        )

        elemento_activo = page.evaluate("""
            () => document.activeElement &&
                  document.activeElement.getAttribute('placeholder')
        """)

        print("Elemento activo después de escribir:", elemento_activo)

        if elemento_activo != "Descripción, ID...":
            page.screenshot(
                path=RUTA_EVIDENCIA + "REG-PW-004_03_error_perdida_foco.png"
            )
            browser.close()
            raise AssertionError(
                "El buscador de reportes pierde el foco después de escribir una letra."
            )

        buscador.press("e")
        buscador.press("n")
        buscador.press("t")

        page.wait_for_timeout(1000)

        page.screenshot(
            path=RUTA_EVIDENCIA + "REG-PW-004_04_busqueda_completa.png"
        )

        print("✔ REG-PW-004 ejecutado: Live Search Reportes.")

        input("Presioná ENTER para cerrar...")
        browser.close()