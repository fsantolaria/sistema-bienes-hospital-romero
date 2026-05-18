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


def test_reg_pw_005_filtro_guardia_limpieza():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=250)

        page = browser.new_page(
            viewport={"width": 1366, "height": 768}
        )

        # LOGIN
        page.goto(
            "http://127.0.0.1:8000/inicio/",
            wait_until="domcontentloaded"
        )

        ocultar_debug_toolbar(page)

        try:
            page.get_by_role(
                "button",
                name="Administrador"
            ).click(timeout=2000)

        except Exception:
            print("Botón Administrador no encontrado.")

        page.locator(
            "input[name='usuario'], input[name='username']"
        ).fill("admin")

        page.locator(
            "input[type='password']"
        ).fill("Hospital@1")

        page.keyboard.press("Enter")

        page.wait_for_timeout(2000)

        # IR A REPORTES
        page.goto(
            "http://127.0.0.1:8000/reportes/",
            wait_until="domcontentloaded"
        )

        ocultar_debug_toolbar(page)

        page.screenshot(
            path=RUTA_EVIDENCIA +
            "REG-PW-005_01_pantalla_reportes.png"
        )

        # FILTRO AREA GUARDIA
        selector_servicio = page.get_by_placeholder(
            "Buscar servicio..."
        )

        selector_servicio.click()

        selector_servicio.fill("Area Guardia")

        page.wait_for_timeout(1000)

        page.keyboard.press("Enter")

        page.wait_for_timeout(2000)

        page.screenshot(
            path=RUTA_EVIDENCIA +
            "REG-PW-005_02_filtro_guardia.png"
        )

        # VALIDAR CONTENIDO TABLA
        contenido_tabla = page.locator("table").inner_text()

        print("Contenido tabla:")
        print(contenido_tabla)

        # VALIDAR QUE EXISTA AREA GUARDIA
        if "Area Guardia" not in contenido_tabla:

            page.screenshot(
                path=RUTA_EVIDENCIA +
                "REG-PW-005_03_error_no_guardia.png"
            )

            browser.close()

            raise AssertionError(
                "No se muestran bienes de Area Guardia."
            )

        # VALIDAR BUG:
        # NO DEBERIA MOSTRAR LIMPIEZA
        if "Area Limpieza Hospitalaria" in contenido_tabla:

            page.screenshot(
                path=RUTA_EVIDENCIA +
                "REG-PW-005_04_error_muestra_limpieza.png"
            )

            browser.close()

            raise AssertionError(
                "El filtro Area Guardia muestra bienes "
                "de Area Limpieza Hospitalaria."
            )

        page.screenshot(
            path=RUTA_EVIDENCIA +
            "REG-PW-005_05_validacion_ok.png"
        )

        print(
            "✔ REG-PW-005 ejecutado correctamente."
        )

        input("Presioná ENTER para cerrar...")

        browser.close()