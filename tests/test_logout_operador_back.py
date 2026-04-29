from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# =========================
# CONFIGURACIÓN
# =========================
options = Options()
options.binary_location = "/usr/bin/chromium-browser"

service = Service("/usr/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=options)

BASE_URL = "http://127.0.0.1:8000"

# =========================
# OPERADOR
# =========================
operador_user = "beatrizsalazar"
operador_pass = "romero1325"


def login_operador():
    driver.get(f"{BASE_URL}/login/")

    driver.find_element(By.NAME, "usuario").send_keys(operador_user)
    driver.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys(operador_pass)
    driver.find_element(By.TAG_NAME, "form").submit()

    time.sleep(4)

    print("✔ Operador logueado:", driver.current_url)

    assert "/home" in driver.current_url or "/inicio" in driver.current_url


def logout_operador():
    driver.get(f"{BASE_URL}/logout/")
    time.sleep(4)

    print("✔ Logout realizado:", driver.current_url)


def test_back_no_reingreso():
    # intenta volver atrás
    driver.back()
    time.sleep(4)

    print("URL después de BACK:", driver.current_url)

    # intenta refrescar por si acaso
    driver.refresh()
    time.sleep(4)

    print("URL después de REFRESH:", driver.current_url)

    # VALIDACIÓN: no debe volver al home del operador
    assert "/login" in driver.current_url or "/inicio" in driver.current_url

    print("✔ Seguridad OK: no puede reingresar con BACK")


# =========================
# EJECUCIÓN
# =========================
try:
    login_operador()
    logout_operador()
    test_back_no_reingreso()

    print("✔ TEST COMPLETO OK: sesión protegida")

    input("Presioná Enter para cerrar...")

finally:
    driver.quit()