from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def test_back_logout():

    options = Options()
    options.binary_location = "/usr/bin/chromium-browser"
    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)

    # Abrir sistema
    driver.get("http://127.0.0.1:8000")
    time.sleep(2)

    # Login como ADMIN
    botones = driver.find_elements(By.XPATH, "//*[contains(.,'Administrador')]")
    for b in botones:
        if b.is_displayed():
            driver.execute_script("arguments[0].click();", b)
            break

    time.sleep(3)

    # Logout
    driver.get("http://127.0.0.1:8000/logout/")
    time.sleep(2)

    # Intentar volver atrás
    driver.back()
    time.sleep(2)

    print("URL actual:", driver.current_url)

    # Validación clave
    assert "/inicio/" not in driver.current_url

    print("✔ TEST OK: no permite volver atrás")

    driver.quit()


test_back_logout()