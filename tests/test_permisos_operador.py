from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def test_permiso_operador():

    options = Options()
    options.binary_location = "/usr/bin/chromium-browser"
    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)

    # 1. Entrar al sistema
    driver.get("http://127.0.0.1:8000")
    time.sleep(2)

    # 2. LOGIN COMO OPERADOR
    botones = driver.find_elements(By.XPATH, "//*[contains(.,'Operador')]")
    for b in botones:
        if b.is_displayed():
            driver.execute_script("arguments[0].click();", b)
            break

    time.sleep(3)

    # 3. Intentar dar de alta al operador otro operador 
    driver.get("http://127.0.0.1:8000/operadores/alta/")
    time.sleep(2)

    print("URL operador:", driver.current_url)

    # 4. VALIDACIÓN
    assert "/operadores/alta/" not in driver.current_url

    print("✔ TEST OK: operador NO puede acceder a alta")

    driver.quit()


test_permiso_operador()