from playwright.sync_api import sync_playwright
import os

RUTA_EVIDENCIA = "QA_Regresion/evidencias/playwright/alta_bien/"
os.makedirs(RUTA_EVIDENCIA, exist_ok=True)


def ocultar_debug_toolbar(page):
    page.evaluate("""
        const toolbar = document.getElementById('djDebug');
        if (toolbar) toolbar.style.display = 'none';
    """)


def test_reg_pw_001_alta_bien_exitosa():
    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False,
            slow_mo=150
        )

        page = browser.new_page(
            viewport={"width": 1366, "height": 768}
        )

        # =====================================================
        # 1. LOGIN
        # =====================================================

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

        # =====================================================
        # 2. INGRESAR A ALTA DE BIEN
        # =====================================================

        page.goto(
            "http://127.0.0.1:8000/bienes/",
            wait_until="domcontentloaded"
        )

        ocultar_debug_toolbar(page)

        # =====================================================
        # EVIDENCIA 1
        # Formulario vacío
        # =====================================================

        page.screenshot(
            path=RUTA_EVIDENCIA +
            "REG-PW-001_01_formulario_vacio.png"
        )

        # =====================================================
        # 3. COMPLETAR FORMULARIO
        # =====================================================

        # Descripción
        page.locator("textarea").nth(0).fill(
            "Monitor Samsung 24 pulgadas"
        )

        # Cantidad
        cantidad = page.get_by_label("Cantidad")
        cantidad.click()
        cantidad.press("Control+A")
        cantidad.press("Backspace")
        cantidad.press("1")

        # Origen
        page.locator("select").nth(0).select_option(index=1)

        # Estado
        page.locator("select").nth(1).select_option(label="Activo")

        # Servicios / Sector
        page.locator("select").nth(2).select_option(index=1)

        # Cuenta Código
        page.get_by_label("Cuenta Código").fill("CC-2026")

        # Nomenclatura
        page.get_by_label("Nomenclatura").fill("MON-24")

        # Número de Serie
        page.get_by_label("N° de Serie").fill("SERIE-001")

        # Número de ID
        page.get_by_label("N° de ID").fill("ID-001")

        # SIEM
        #page.get_by_label("SIEM").fill("SIEM-001")

        # Fecha Alta
        #page.get_by_label("Fecha de Alta").fill("2026-05-15")

        # Observaciones
        page.locator("textarea").nth(1).fill(
          "Alta QA automatizada Playwright"
        )

        # Expediente
        page.get_by_label("N° de Expediente").fill("EXP-2026")

        # Compra
        page.get_by_label("N° de Compra").fill("COMP-2026")

        # =====================================================
        # EVIDENCIA 2
        # Formulario completo
        # =====================================================

        page.screenshot(
            path=RUTA_EVIDENCIA +
            "REG-PW-001_02_formulario_completo.png"
        )

        # =====================================================
        # 4. GUARDAR BIEN
        # =====================================================

        page.get_by_role(
            "button",
            name="Guardar bien"
        ).click()

        page.wait_for_timeout(3000)

        # =====================================================
        # EVIDENCIA 3
        # Resultado final
        # =====================================================

        page.screenshot(
            path=RUTA_EVIDENCIA +
            "REG-PW-001_03_resultado_guardado.png"
        )

        print(
            "✔ PW-001 ejecutado correctamente: Alta de Bien."
        )

        input("Presioná ENTER para cerrar...")

        browser.close()