from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

try:
    print("Abriendo login...")
    driver.get("http://127.0.0.1:8000/login/")

    print("Esperando campo usuario...")
    campo_usuario = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder,'usuario')]"))
    )

    print("Esperando campo contraseña...")
    campo_password = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder,'contraseña')]"))
    )

    print("Completando login...")
    campo_usuario.send_keys("milagritos")
    campo_password.send_keys("123456789")
    time.sleep(1)

    boton_login = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button"))
)
    

    print("Haciendo click en ingresar...")
    driver.execute_script("arguments[0].click();", boton_login)
    time.sleep(3)

    print("Entrando a Operadores...")

    botones = driver.find_elements(By.TAG_NAME, "button")

    for boton in botones:
      if "Operadores" in boton.text:
        driver.execute_script("arguments[0].click();", boton)
        break

    time.sleep(3)

    print("Ir a alta de operador...")
    driver.get("http://127.0.0.1:8000/operadores/alta/")
    time.sleep(2)

    print("Llegó al formulario de alta")
    print("Completando formulario con DNI duplicado...")

    driver.find_element(By.NAME, "nombre").send_keys("maria")
    driver.find_element(By.NAME, "apellido").send_keys("perez")

    driver.find_element(
    By.XPATH,
    "//*[contains(normalize-space(.), 'Número de Documento')]/following::input[1]"
    ).send_keys("11115556")

    driver.find_element(
    By.XPATH,
    "//*[contains(normalize-space(.), 'Email')]/following::input[1]"
    ).send_keys("testnuevo5@mail.com")

    driver.find_element(
    By.XPATH,
    "//*[contains(normalize-space(.), 'Contraseña')]/following::input[1]"
    ).send_keys("1234")

    time.sleep(1)

    print("Intentando guardar...")
    driver.find_element(By.XPATH, "//button[contains(., 'Guardar')]").click()
    time.sleep(3)

    if "alta" in driver.current_url:
        print("✔ El sistema permaneció en alta. Posible bloqueo correcto por DNI duplicado.")
    else:
        print("❌ El sistema salió del formulario. Posible error: permitió guardar.")
        print("Validando resultado...")

except Exception as e:
    print("❌ ERROR:", e)

input("Presioná Enter para cerrar...")
driver.quit()