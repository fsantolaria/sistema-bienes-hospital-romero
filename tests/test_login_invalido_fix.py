from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def test_login_invalido():

    options = Options()
    options.binary_location = "/usr/bin/chromium-browser"
    options.add_argument("--incognito")
    service = Service("/usr/bin/chromedriver")

    driver = webdriver.Chrome(service=service, options=options)

    driver.get("http://127.0.0.1:8000/login/")
    time.sleep(2)

    # Campos correctos
    usuario = driver.find_element(By.NAME, "usuario")
    contrasena = driver.find_element(By.NAME, "contrasena")

    usuario.send_keys("falso")
    contrasena.send_keys("1234")

    contrasena.submit()

    time.sleep(3)

    print("URL después:", driver.current_url)

    # ✅ VALIDACIÓN FINAL
    assert "login" in driver.current_url

    print("✔ TEST OK: login inválido bloqueado correctamente")

    driver.quit()


test_login_invalido()