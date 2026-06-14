from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

def test_login():
    options = Options()
    options.binary_location = "/usr/bin/chromium-browser"

    service = Service("/usr/bin/chromedriver")

    driver = webdriver.Chrome(service=service, options=options)

    driver.get("http://127.0.0.1:8000")

    wait = WebDriverWait(driver, 10)

    assert "127.0.0.1" in driver.current_url
    print("✔ Login cargado correctamente")

    driver.quit()

if __name__ == "__main__":
    test_login()