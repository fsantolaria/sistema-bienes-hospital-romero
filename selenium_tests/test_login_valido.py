from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()

try:
    print("Abriendo sistema...")
    driver.get("http://127.0.0.1:8000/inicio/")
    time.sleep(2)

    print("Entrando a Administrador...")
    boton_admin = driver.find_element(By.XPATH, "//button[contains(text(),'Administrador')]")
    boton_admin.click()
    time.sleep(2)

    print("Completando login...")
    usuario = driver.find_element(By.NAME, "username")
    password = driver.find_element(By.NAME, "password")

    usuario.send_keys("admin")
    password.send_keys("admin123")
    password.send_keys(Keys.RETURN)

    time.sleep(3)

    print("Login automatizado ejecutado")
    input("Presioná Enter para cerrar...")

except Exception as e:
    print("❌ ERROR:", e)
    input("Hubo un error. Presioná Enter para cerrar...")

finally:
    driver.quit()