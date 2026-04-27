from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

try:
    print("Abriendo sistema...")
    driver.get("http://127.0.0.1:8000/inicio/")
    time.sleep(3)

    # Click en Administrador
    boton_admin = driver.find_element(By.XPATH, "//button[contains(text(),'Administrador')]")
    boton_admin.click()
    time.sleep(2)

    print("Ingresando datos incorrectos...")

    # Buscar campos
    usuario = driver.find_element(By.NAME, "username")
    contraseña = driver.find_element(By.NAME, "password")

    # Datos incorrectos
    usuario.send_keys("usuario_falso")
    contraseña.send_keys("1234")

    # Click en ingresar
    boton_login = driver.find_element(By.XPATH, "//button[contains(text(),'Ingresar')]")
    boton_login.click()
    time.sleep(3)

    print("Validando que NO ingresó...")

    # Validación (sigue en login)
    if "login" in driver.current_url:
        print("Login inválido validado correctamente")
    else:
        print("ERROR: ingresó cuando no debía")

except Exception as e:
    print("❌ ERROR:", e)

input("Presioná Enter para cerrar...")

driver.quit()