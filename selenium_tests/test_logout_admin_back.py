from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.binary_location = "/usr/bin/chromium-browser"

service = Service("/usr/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=options)

BASE_URL = "http://127.0.0.1:8000"

usuario_admin = "bea22"
password_admin = "romero2213"


def test_login_admin():
    driver.get(f"{BASE_URL}/login/")

    driver.find_element(By.NAME, "usuario").send_keys(usuario_admin)
    driver.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys(password_admin)

    driver.find_element(By.TAG_NAME, "form").submit()

    time.sleep(4)

    print("URL después login:", driver.current_url)
    assert "/home_admin/" in driver.current_url


def test_logout_admin():
    driver.get(f"{BASE_URL}/logout/")

    time.sleep(4)

    print("URL después logout:", driver.current_url)
    assert "/login/" in driver.current_url


def test_acceso_sin_login():
    driver.get(f"{BASE_URL}/home_admin/")

    time.sleep(4)

    print("URL intento acceso:", driver.current_url)
    assert "/login/" in driver.current_url


try:
    test_login_admin()
    test_logout_admin()
    test_acceso_sin_login()

    print("✔ TEST OK: flujo de seguridad correcto")

    input("Presioná Enter para cerrar...")

finally:
    driver.quit()