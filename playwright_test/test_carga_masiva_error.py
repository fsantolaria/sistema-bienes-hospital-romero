from playwright.sync_api import sync_playwright

URL_LOGIN = "http://127.0.0.1:8000/login/"
URL_BIENES = "http://127.0.0.1:8000/bienes/"

USUARIO = "mili"
PASSWORD = "mmmb123456"

ARCHIVO_INVALIDO = r"C:\Users\milim\Downloads\image_f0e8888a.png"


def test_carga_masiva_archivo_invalido():
    with sync_playwright() as p:
        print("Abriendo navegador...")

        browser = p.chromium.launch(
            headless=False,
            slow_mo=700,
            args=["--start-maximized"]
        )

        context = browser.new_context(no_viewport=True)
        page = context.new_page()

        print("Entrando al login...")
        page.goto(URL_LOGIN)

        print("Completando usuario y contraseña...")
        page.get_by_placeholder("Ingrese su usuario").fill(USUARIO)
        page.get_by_placeholder("Ingrese su contraseña").fill(PASSWORD)
        page.get_by_role("button", name="Iniciar Sesión").click()

        page.wait_for_timeout(2500)

        print("Entrando a Bienes...")
        page.goto(URL_BIENES)
        page.wait_for_timeout(2000)

        print("Entrando a Carga masiva...")
        page.get_by_role("link", name="Carga masiva").click()
        page.wait_for_timeout(2000)

        print("Subiendo archivo inválido...")
        page.set_input_files('input[type="file"]', ARCHIVO_INVALIDO)
        page.wait_for_timeout(2000)

        page.get_by_text("Procesar Archivo(s)").click()
        page.wait_for_timeout(2000)

        page.screenshot(path="QA_Evidencias/Sprint2/Sprint_Actual_Playwright/CP-PW-041_02_error_archivo_invalido.png")

        print("Archivo PNG seleccionado. Verificá en pantalla si el sistema lo rechaza o lo acepta.")

        input("Presioná ENTER para cerrar el navegador...")
        browser.close()


test_carga_masiva_archivo_invalido()