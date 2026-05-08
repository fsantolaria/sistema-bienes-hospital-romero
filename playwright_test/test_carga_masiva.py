from playwright.sync_api import sync_playwright

def test_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()

        # Login
        page.goto("http://127.0.0.1:8000/login/")
        page.get_by_label("Usuario").fill("mili")
        page.get_by_label("Contraseña").fill("123456789")
        page.get_by_text("Iniciar sesión").click()
        page.wait_for_timeout(3000)

        # Entrar a Bienes Patrimoniales
        page.get_by_role("link", name="Bienes Patrimoniales").click()
        page.wait_for_timeout(3000)

        # Entrar a Carga masiva
        page.get_by_text("Carga masiva").click()
        page.wait_for_timeout(3000)

        # Subir archivo Excel
        page.set_input_files(
            'input[type="file"]',
            'C:/Users/milim/Downloads/RELEVAMIENTO_TEATRO_POLO_LEFEUDO_ordenado.xlsx'
        )
        page.wait_for_timeout(2000)

        # Procesar archivo
        page.locator("button:has-text('Procesar')").click()
        page.wait_for_timeout(5000)

        # Evidencia
        page.screenshot(
            path="QA_Evidencias/Sprint2/Sprint_Actual_Playwright/CP-PW-003_resultado_carga.png"
        )

        input("Presiona ENTER para cerrar")
        browser.close()

test_login()