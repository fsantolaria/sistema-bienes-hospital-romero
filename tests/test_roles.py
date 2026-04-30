from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

def test_operador_no_puede_alta_operador():
    options = Options()
    options.binary_location = "/usr/bin/chromium-browser"

    service = Service("/usr/bin/chromedriver")

    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 10)

    # 🟢 1. entrar como OPERADOR
    driver.get("http://127.0.0.1:8000")

    botones = driver.find_elements(By.XPATH, "//*[contains(.,'Operador')]")
    for b in botones:
        if b.is_displayed():
            driver.execute_script("arguments[0].click();", b)
            break

    wait.until(lambda d: "/inicio/" in d.current_url)

    print("✔ Entró como operador")

    # 🔴 2. intentar acceder a ALTA DE OPERADOR
    driver.get("http://127.0.0.1:8000/operadores/alta/")

    print("URL después del intento:", driver.current_url)

    # 🧪 3. VALIDACIÓN DE SEGURIDAD
    assert "/operadores/alta/" not in driver.current_url

    print("✔ SEGURIDAD OK: operador NO puede dar de alta operadores")

    driver.quit()


if __name__ == "__main__":
    test_operador_no_puede_alta_operador()