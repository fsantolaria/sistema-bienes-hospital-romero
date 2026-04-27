from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

driver = webdriver.Chrome()

try:
    print("1. Abriendo login...")
    driver.get("http://127.0.0.1:8000/login/")
    driver.maximize_window()
    time.sleep(2)

    print("2. Buscando campos de login...")
    usuario = driver.find_element(By.ID, "usuario")
    password = driver.find_element(By.XPATH, "//input[@type='password']")

    print("3. Ingresando credenciales...")
    usuario.click()
    usuario.send_keys("milagritos")
    time.sleep(1)

    password.click()
    password.send_keys("123456789")   # cambiá si tu contraseña real es otra
    time.sleep(1)

    print("4. Enviando formulario...")
    password.send_keys(Keys.ENTER)
    time.sleep(4)

    print("5. Entrando a bienes...")
    driver.get("http://127.0.0.1:8000/bienes/")
    time.sleep(4)

    print("6. Completando campos básicos...")

    descripcion = driver.find_element(By.NAME, "descripcion")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", descripcion)
    time.sleep(1)
    descripcion.click()
    descripcion.clear()
    descripcion.send_keys("Notebook HP")
    time.sleep(1)

    valor_descripcion = descripcion.get_attribute("value")
    if not valor_descripcion.strip():
        print("La descripción no se escribió, reintentando...")
        descripcion.click()
        descripcion.send_keys("Notebook HP")
        time.sleep(1)

    cantidad = driver.find_element(By.NAME, "cantidad")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", cantidad)
    time.sleep(1)
    cantidad.click()
    cantidad.clear()
    cantidad.send_keys("1")
    time.sleep(2)

    print("7. Bajando hasta el botón Guardar bien...")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    boton_guardar = driver.find_element(By.XPATH, "//button[contains(., 'Guardar bien')]")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", boton_guardar)
    time.sleep(2)

    ActionChains(driver).move_to_element(boton_guardar).click().perform()
    time.sleep(3)

    print("8. Revisar qué pasó después de guardar...")
    print("URL actual:", driver.current_url)

    input("Presioná Enter para cerrar...")

except Exception as e:
    print("❌ ERROR:")
    print(e)
    input("Presioná Enter para cerrar...")

finally:
    driver.quit()