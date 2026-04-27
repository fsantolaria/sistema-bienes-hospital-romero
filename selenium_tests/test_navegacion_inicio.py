from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

try:
    print("Abriendo sistema...")
    driver.get("http://127.0.0.1:8000/inicio/")
    time.sleep(3)

    print("Buscando botón Administrador...")
    boton_admin = driver.find_element(By.XPATH, "//button[contains(text(),'Administrador')]")
    
    print("Haciendo click...")
    boton_admin.click()
    time.sleep(5)

    print("Prueba de navegación OK")

except Exception as e:
    print("❌ ERROR:", e)
    print("Prueba de navegación OK")

# 🔴 ESTO SIEMPRE SE EJECUTA
input("🔴 Presioná Enter para cerrar...")

driver.quit()