from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login_y_validar(driver, wait, usuario, password, rol):

    driver.get("http://127.0.0.1:8000/login/")

    # campo usuario
    wait.until(EC.presence_of_element_located((By.NAME, "usuario"))).send_keys(usuario)

    # campo password (usamos XPath para evitar errores)
    wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))).send_keys(password)

    # botón login
    driver.find_element(By.TAG_NAME, "button").click()

    # esperar redirección
    wait.until(EC.url_changes("http://127.0.0.1:8000/login/"))

    url = driver.current_url
    print(f"URL {rol.upper()}:", url)

    # validación por rol
    if rol == "admin" and "/home_admin" in url:
        print("✔ Admin redirigido correctamente")

    elif rol == "operador" and "operador" in url:
        print("✔ Operador redirigido correctamente")

    elif rol == "supervisor" and "supervisor" in url:
        print("✔ Supervisor redirigido correctamente")

    else:
        print(f"❌ Error redirección {rol}")

    # logout
    driver.get("http://127.0.0.1:8000/logout/")


def test_redireccion_roles():

    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    # ===== ADMIN =====
    login_y_validar(driver, wait, "bea22", "romero2513", "admin")

    # ===== SUPERVISOR =====
    login_y_validar(driver, wait, "gonzaloromero", "romero2513", "supervisor")

    # ===== OPERADOR =====
    login_y_validar(driver, wait, "nataliaromero", "romero2513", "operador")

    driver.quit()


if __name__ == "__main__":
    test_redireccion_roles()