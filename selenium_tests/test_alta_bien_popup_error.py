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

    print("2. Buscando campos...")
    usuario = driver.find_element(By.ID, "usuario")
    password = driver.find_element(By.XPATH, "//input[@type='password']")

    print("3. Escribiendo credenciales...")
    usuario.click()
    usuario.send_keys("milagritos")
    time.sleep(1)

    password.click()
    password.send_keys("123456789")   # cambiá si tu contraseña real es otra
    time.sleep(1)

    print("4. Enviando formulario...")
    password.send_keys(Keys.ENTER)
    time.sleep(4)

    print("5. Login OK. URL actual:", driver.current_url)

    print("6. Entrando directo a /bienes/ ...")
    driver.get("http://127.0.0.1:8000/bienes/")
    time.sleep(4)

    print("7. Ya estamos en Alta de Bien. URL actual:", driver.current_url)

    print("8. Bajando hasta el final de la página...")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    print("9. Buscando botón Guardar bien...")
    boton_guardar = driver.find_element(By.XPATH, "//button[contains(., 'Guardar bien')]")

    print("10. Centrando el botón en pantalla...")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", boton_guardar)
    time.sleep(2)

    print("11. Haciendo click en Guardar bien...")
    ActionChains(driver).move_to_element(boton_guardar).click().perform()
    time.sleep(3)

    print("12. Validando si apareció un popup de error...")
    popup = driver.find_element(By.XPATH, "//*[contains(text(),'No se pudo')]")

    if popup.is_displayed():
        print("✅ Popup de error validado correctamente")
    else:
        print("❌ No apareció el popup")

    input("Presioná Enter para cerrar...")

except Exception as e:
    print("❌ ERROR:")
    print(e)
    input("Presioná Enter para cerrar...")

finally:
    driver.quit()