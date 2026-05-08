from pathlib import Path
from playwright.sync_api import sync_playwright

URL_LOGIN = "http://127.0.0.1:8000/login/"
URL_INICIO = "http://127.0.0.1:8000/inicio/"

USUARIO = "mili"
PASSWORD = "mmmb123456"

EVIDENCIAS = Path("QA_Evidencias/Sprint2/Sprint_Actual_Playwright")
EVIDENCIAS.mkdir(parents=True, exist_ok=True)


def hay_texto_visible(page, texto):
    return page.locator(f"text={texto}").evaluate_all("""
        els => els.some(e => {
            const r = e.getBoundingClientRect();
            return r.width > 0 && r.height > 0;
        })
    """)


def test_notificaciones():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500, args=["--start-maximized"])
        context = browser.new_context(no_viewport=True)
        page = context.new_page()

        page.goto(URL_LOGIN)
        page.get_by_placeholder("Ingrese su usuario").fill(USUARIO)
        page.get_by_placeholder("Ingrese su contraseña").fill(PASSWORD)
        page.get_by_role("button", name="Iniciar Sesión").click()

        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1500)

        page.goto(URL_INICIO)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1500)

        if page.get_by_text("Ocultar »").count() > 0:
            page.get_by_text("Ocultar »").click()
            page.wait_for_timeout(500)

        page.screenshot(path=EVIDENCIAS / "CP-PW-004_00_inicio.png")

        # Abrir campanita
       # ABRIR CAMPANITA usando el contador rojo
        contador = page.locator("text=/^\\d+$/").first
        contador.wait_for(state="visible", timeout=10000)
        contador.click(force=True)

        page.wait_for_timeout(1500)
        page.screenshot(path=EVIDENCIAS / "CP-PW-004_01_panel_abierto.png")
        if hay_texto_visible(page, "Notificaciones"):
           print("Panel de notificaciones abierto correctamente")
        else:
           print("ERROR: No se abrió el panel de notificaciones")

        if page.get_by_text("Marcar como leída").count() > 0:
            page.get_by_text("Marcar como leída").first.click()
            page.wait_for_timeout(1000)
            page.screenshot(path=EVIDENCIAS / "CP-PW-004_02_marcar_como_leida.png")

        if page.get_by_text("Marcar todas").count() > 0:
            page.get_by_text("Marcar todas").first.click()
            page.wait_for_timeout(1000)
            page.screenshot(path=EVIDENCIAS / "CP-PW-004_03_marcar_todas.png")

        if page.get_by_text("Borrar todas").count() > 0:
            page.get_by_text("Borrar todas").first.click()
            page.wait_for_timeout(1000)
            page.screenshot(path=EVIDENCIAS / "CP-PW-004_04_borrar_todas.png")

        print("TEST DE NOTIFICACIONES FINALIZADO")
        input("Presioná ENTER para cerrar...")
        browser.close()


test_notificaciones()