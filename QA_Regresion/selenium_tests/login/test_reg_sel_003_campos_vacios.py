from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

RUTA_EVIDENCIA = "QA_Regresion/evidencias/selenium/login/"
os.makedirs(RUTA_EVIDENCIA, exist_ok=True)

def ocultar_debug_toolbar(driver):
    driver.execute_script("""
        let toolbar = document.getElementById('djDebug');
        if (toolbar) {
            toolbar.style.display = 'none';
        }
    """)

def test_reg_sel_003_campos_vacios():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    driver.set_window_size(1366, 768)

    try:
        driver.get("http://127.0.0.1:8000/inicio/")
        time.sleep(2)

        ocultar_debug_toolbar(driver)
        driver.execute_script("document.body.style.zoom='80%'")

        try:
            boton_admin = driver.find_element(By.XPATH, "//button[contains(text(),'Administrador')]")
            boton_admin.click()
            time.sleep(2)
        except:
            print("No se encontró botón Administrador, se continúa con el formulario visible.")

        usuario = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@name='usuario' or @name='username']")
            )
        )

        password = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@type='password' or @name='password']")
            )
        )

        usuario.clear()
        password.clear()

        password.send_keys(Keys.RETURN)

        time.sleep(3)

        ocultar_debug_toolbar(driver)
        driver.execute_script("document.body.style.zoom='80%'")

        driver.save_screenshot(RUTA_EVIDENCIA + "REG-SEL-003_01_campos_vacios.png")

        assert (
            "login" in driver.current_url.lower()
            or "inicio" in driver.current_url.lower()
        ), "El sistema permitió acceso con campos vacíos."

        print("✔ Validación de campos vacíos ejecutada correctamente.")

        input("Presioná ENTER para cerrar...")

    finally:
        driver.quit()