from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()

try:
    print("1. Abriendo login...")
    driver.get("http://127.0.0.1:8000/login/")
    driver.maximize_window()
    time.sleep(3)

    print("2. Ingresando credenciales...")
    usuario = driver.find_element(By.ID, "usuario")
    password = driver.find_element(By.XPATH, "//input[@type='password']")

    usuario.send_keys("milagritos")
    password.send_keys("123456789")   # cambiá si tu contraseña real es otra
    password.send_keys(Keys.ENTER)
    time.sleep(4)

    print("3. Entrando directo a la lista de bienes...")
    driver.get("http://127.0.0.1:8000/lista-bienes/")
    time.sleep(4)

    print("4. URL actual:", driver.current_url)

    print("5. Buscando botón editar...")
    boton_editar = driver.find_element(By.XPATH, "//a[contains(@href, '/bienes/') and contains(@href, '/editar/')]")
    driver.execute_script("arguments[0].click();", boton_editar)
    time.sleep(4)

    print("6. Modificando descripción...")
    descripcion = driver.find_element(By.NAME, "descripcion")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", descripcion)
    time.sleep(1)
    descripcion.click()
    descripcion.clear()
    descripcion.send_keys("Bien modificado Selenium")
    time.sleep(2)

    print("7. Guardando cambios...")
    boton_guardar = driver.find_element(By.XPATH, "//button[contains(., 'Guardar')]")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", boton_guardar)
    time.sleep(2)
    driver.execute_script("arguments[0].click();", boton_guardar)
    time.sleep(4)

    print("8. Validando resultado...")
    pagina = driver.page_source.lower()

    if "modificado" in pagina or "éxito" in pagina or "exitosa" in pagina:
        print("✅ Modificación exitosa validada correctamente")
    else:
        print("⚠️ No se detectó mensaje claro de éxito")

    print("URL final:", driver.current_url)
    input("Presioná Enter para cerrar...")

except Exception as e:
    print("❌ ERROR REAL:")
    print(repr(e))
    input("Presioná Enter para cerrar...")

finally:
    driver.quit()