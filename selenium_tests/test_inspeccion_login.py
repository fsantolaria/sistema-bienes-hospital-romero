from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)

try:
    driver.get("http://127.0.0.1:8000/login/")
    time.sleep(2)

    print("=== INPUTS ===")
    inputs = driver.find_elements(By.TAG_NAME, "input")
    for i, inp in enumerate(inputs):
        print(
            i,
            "type=", inp.get_attribute("type"),
            "| name=", inp.get_attribute("name"),
            "| id=", inp.get_attribute("id"),
            "| placeholder=", inp.get_attribute("placeholder")
        )

    print("\n=== BUTTONS ===")
    buttons = driver.find_elements(By.TAG_NAME, "button")
    for i, btn in enumerate(buttons):
        print(
            i,
            "text=", btn.text,
            "| type=", btn.get_attribute("type"),
            "| id=", btn.get_attribute("id"),
            "| class=", btn.get_attribute("class")
        )

    print("\n=== FORMS ===")
    forms = driver.find_elements(By.TAG_NAME, "form")
    print("Cantidad de forms:", len(forms))
    for i, form in enumerate(forms):
        print(i, form.get_attribute("outerHTML")[:500])

    input("Presioná Enter para cerrar...")

finally:
    driver.quit()