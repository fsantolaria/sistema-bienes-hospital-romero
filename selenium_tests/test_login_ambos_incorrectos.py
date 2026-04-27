from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

try:
    print("Abriendo sistema...")
    driver.get("http://127.0.0.1:8000/inicio/")
    time.sleep(2)

    print("Ingresando al login de administrador...")
    boton_admin = driver.find_element(By.XPATH, "//button[contains(text(),'Administrador')]")
    boton_admin.click()
    time.sleep(2)

    print("Ingresando usuario y contraseña incorrectos...")
    usuario = driver.find_element(By.NAME, "username")
    password = driver.find_element(By.NAME, "password")

    usuario.send_keys("usuario_incorrecto")
    password.send_keys("clave_incorrecta")

    print("Intentando iniciar sesión...")
    boton_login = driver.find_element(By.XPATH, "//button[contains(text(),'Ingresar')]")
    boton_login.click()
    time.sleep(3)

    print("Resultado observado:")
    print("El sistema no ingresa, no muestra mensaje de error y presenta vibración del formulario.")
    print("Posible bug detectado.")

except Exception as e:
    print("❌ ERROR:", e)

input("Presioná Enter para cerrar...")

driver.quit()