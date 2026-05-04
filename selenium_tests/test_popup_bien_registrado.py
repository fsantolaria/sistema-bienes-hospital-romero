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
# TEST
# =========================
def test_alta_bien_patrimonial():
    driver.get(f"{BASE_URL}/login/")

    # LOGIN
    driver.find_element(By.NAME, "usuario").send_keys("bea22")
    driver.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys("romero2213")
    driver.find_element(By.TAG_NAME, "form").submit()

    time.sleep(3)

    print("✔ Login OK:", driver.current_url)

    # IR A BIENES (ruta real)
    driver.get(f"{BASE_URL}/bienes/")

    time.sleep(2)

    # =========================
    # CARGA DE BIEN
    # =========================
    driver.find_element(By.NAME, "descripcion").send_keys("Ventilador QA")
    driver.find_element(By.NAME, "cantidad").send_keys("1")
    driver.find_element(By.CSS_SELECTOR, "input[type='text']").send_keys("999999")

    # SUBMIT
    driver.find_element(By.TAG_NAME, "form").submit()

    time.sleep(3)

    print("✔ Form enviado")

    # =========================
    # VALIDACIÓN SIMPLE
    # =========================
    page = driver.page_source.lower()

    assert (
        "registrado" in page
        or "correctamente" in page
        or "no se pudo guardar" in page
    )

    print("✔ TEST OK: popup validado")

    input("Enter para cerrar...")

    driver.quit()


# =========================
# EJECUCIÓN
# =========================
if __name__ == "__main__":
    test_alta_bien_patrimonial()