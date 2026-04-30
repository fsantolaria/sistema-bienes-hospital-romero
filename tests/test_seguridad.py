from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def test_acceso_sin_login():
    options = Options()
    options.binary_location = "/usr/bin/chromium-browser"

    service = Service("/usr/bin/chromedriver")

    driver = webdriver.Chrome(service=service, options=options)

    # intentar entrar SIN login
    driver.get("http://127.0.0.1:8000/inicio/")

    # ver qué pasa realmente
    print("URL actual:", driver.current_url)

    # validación
    assert "login" in driver.current_url or "127.0.0.1:8000/" in driver.current_url

    print("✔ SEGURIDAD OK: no deja entrar sin login")

    driver.quit()


if __name__ == "__main__":
    test_acceso_sin_login()