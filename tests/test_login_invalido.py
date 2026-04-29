from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_login_invalido():
    options = Options()
    options.binary_location = "/usr/bin/chromium-browser"

    service = Service("/usr/bin/chromedriver")

    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 10)

    # 🟢 abrir sistema
    driver.get("http://127.0.0.1:8000")

    # 🔴 intentar login incorrecto
    # (esto depende de tu sistema, por ahora simulamos mal acceso)

    # ejemplo: intentar ir directo a inicio sin login
    driver.get("http://127.0.0.1:8000/inicio/")

    print("URL después del intento:", driver.current_url)

    # 🧪 VALIDACIÓN
    assert "/inicio/" not in driver.current_url

    print("✔ LOGIN INVALIDO: acceso denegado correctamente")

    driver.quit()


if __name__ == "__main__":
    test_login_invalido()