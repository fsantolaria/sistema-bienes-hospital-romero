from playwright.sync_api import sync_playwright
import os

RUTA_EVIDENCIA = "QA_Regresion/evidencias/playwright/alta_bien/"
os.makedirs(RUTA_EVIDENCIA, exist_ok=True)


def ocultar_debug_toolbar(page):
    page.evaluate("""
        const toolbar = document.getElementById('djDebug');
        if (toolbar) toolbar.style.display = 'none';
    """)


def test_reg_pw_002_popup_error():

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False,
            slow_mo=150
        )

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

        except:
            print("Botón Administrador no encontrado.")

        page.locator(
            "input[name='usuario'], input[name='username']"
        ).fill("mili")

        page.locator(
            "input[type='password']"
        ).fill("mmmb123456")

        page.keyboard.press("Enter")

        page.wait_for_timeout(2000)

        # IR A BIENES
        page.goto(
            "http://127.0.0.1:8000/bienes/",
            wait_until="domcontentloaded"
        )

        ocultar_debug_toolbar(page)

        # EVIDENCIA 1
        page.screenshot(
            path=RUTA_EVIDENCIA +
            "REG-PW-002_01_formulario_error.png"
        )

        # COMPLETAR FORMULARIO
        page.locator("textarea").nth(0).fill(
            "Ventilador QA"
        )

        cantidad = page.get_by_label("Cantidad")
        cantidad.click()
        cantidad.press("Control+A")
        cantidad.press("Backspace")
        cantidad.press("1")

        # Origen
        page.locator("select").nth(0).select_option(index=1)

        # Estado
        page.locator("select").nth(1).select_option(label="Activo")

        # Servicio
        page.locator("select").nth(2).select_option(index=1)

        # Cuenta Código
        page.get_by_label("Cuenta Código").fill("CC-ERROR")

        # Nomenclatura
        page.get_by_label("Nomenclatura").fill("VENT-ERROR")

        # Número Serie
        page.get_by_label("N° de Serie").fill("SERIE-ERROR")

        # ID DUPLICADO
        page.get_by_label("N° de ID").fill("ID-001")

        # Observaciones
        page.locator("textarea").nth(1).fill(
            "Prueba QA ID duplicado"
        )

        # EVIDENCIA 2
        page.screenshot(
            path=RUTA_EVIDENCIA +
            "REG-PW-002_02_id_duplicado.png"
        )

        # GUARDAR
        page.get_by_role(
            "button",
            name="Guardar bien"
        ).click()

        page.wait_for_timeout(3000)

        # EVIDENCIA 3
        page.screenshot(
            path=RUTA_EVIDENCIA +
            "REG-PW-002_03_popup_error.png"
        )

        print(
            "✔ REG-PW-002 ejecutado correctamente."
        )

        input("Presioná ENTER para cerrar...")

        browser.close()