from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_urls_y_logout():

    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    # =========================
    # TEST 1: URL raíz
    # =========================
    driver.get("http://127.0.0.1:8000/")

    time.sleep(2)

    url_actual = driver.current_url
    print("URL RAÍZ:", url_actual)

    if "/login" in url_actual:
        print("✔ Redirección correcta a login desde raíz")
    else:
        print("❌ Error en redirección desde raíz")

    # =========================
    # TEST 2: LOGIN
    # =========================
    wait.until(EC.presence_of_element_located((By.NAME, "usuario"))).send_keys("bea22")
    wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))).send_keys("romero2513")

    driver.find_element(By.TAG_NAME, "button").click()

    wait.until(EC.url_changes(url_actual))

    print("Login OK:", driver.current_url)

    # =========================
    # TEST 3: LOGOUT
    # =========================
    driver.get("http://127.0.0.1:8000/logout/")
    time.sleep(2)

    url_logout = driver.current_url
    print("Después de logout:", url_logout)

    if "/login" in url_logout:
        print("✔ Logout redirige correctamente a login")
    else:
        print("❌ Error en logout")

    # =========================
    # TEST 4: BOTÓN ATRÁS
    # =========================
    driver.back()
    time.sleep(2)

    url_back = driver.current_url
    print("Después de volver atrás:", url_back)

    if "/login" in url_back:
        print("✔ Seguridad OK: no vuelve a sesión")
    else:
        print("❌ ERROR: vuelve a sesión (falla de seguridad)")

    driver.quit()


if __name__ == "__main__":
    test_urls_y_logout()