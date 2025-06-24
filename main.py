from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from config import LOGIN, PASSWORD, NAME, SURNAME, PESEL, PKK
import time
options = Options()
options.add_argument("window-size=1920,1080")          # ширина 400px, висота 800px
options.add_argument("window-position=1900,100")     # трохи правіше межі екрана

TARGET_DATE = datetime.strptime("26.06.2025", "%d.%m.%Y")

def run_checker():
    # options.add_argument("--headless")  # Розкоментуй для безголового режиму
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 15)

    try:
        # 1. Вхід на сайт
        driver.get("https://info-car.pl/oauth2/login")

        # 2. Чекаємо форми логіна
        wait.until(EC.presence_of_element_located((By.ID, "username")))

        # 3. Вводимо логін та пароль
        driver.find_element(By.ID, "username").send_keys(LOGIN)
        driver.find_element(By.ID, "password").send_keys(PASSWORD)

        # 4. Логін
        driver.find_element(By.ID, "register-button").click()

        # 5. Чекаємо, що сторінка перейшла або завантажилась після входу
        wait.until(EC.url_changes("https://info-car.pl/oauth2/login"))

        # 6. Переходимо напряму на сторінку запису на екзамен
        driver.get("https://info-car.pl/new/prawo-jazdy/zapisz-sie-na-egzamin-na-prawo-jazdy")

        wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Zapisz się na egzamin')]")))

        zapisz_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Zapisz się na egzamin')]")))

        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", zapisz_btn)
        time.sleep(1)

        try:
            zapisz_btn.click()
        except:
            driver.execute_script("arguments[0].click();", zapisz_btn)

        time.sleep(3)

        exam_label = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[@id='exam']")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", exam_label)
        time.sleep(1)
        exam_label.click()
        time.sleep(2)

        try:
            cookie_accept_button = wait.until(EC.element_to_be_clickable((By.ID, "cookiescript_accept")))
            cookie_accept_button.click()
        except:
            print("Повідомлення про cookies не знайдено або вже закрите")

        wait.until(EC.presence_of_element_located((By.ID, "firstname")))

        driver.find_element(By.ID, "firstname").send_keys(NAME)
        driver.find_element(By.ID, "lastname").send_keys(SURNAME)
        driver.find_element(By.ID, "pesel").send_keys(PESEL)
        driver.find_element(By.ID, "pkk").send_keys(PKK)

        category_input = wait.until(EC.element_to_be_clickable((By.ID, "category-select")))
        category_input.click()
        time.sleep(0.5)
        category_input.send_keys("B")
        time.sleep(0.5)
        category_input.send_keys(Keys.ENTER)

        driver.find_element(By.ID, "email").send_keys("kiril4a.mvdk@gmail.com")
        driver.find_element(By.ID, "phoneNumber").send_keys("576568100")

        checkbox = wait.until(EC.element_to_be_clickable((By.ID, "regulations-text")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox)
        time.sleep(0.5)
        checkbox.click()

        next_button = wait.until(EC.element_to_be_clickable((By.ID, "next-btn")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button)
        time.sleep(0.5)
        next_button.click()
        time.sleep(1)

        wait.until(EC.presence_of_element_located((By.ID, "province")))

        province_input = wait.until(EC.element_to_be_clickable((By.ID, "province")))
        province_input.click()
        time.sleep(0.5)
        province_input.clear()
        province_input.send_keys("Dolnośląskie")
        time.sleep(0.5)
        province_input.send_keys(Keys.ENTER)

        wait.until(lambda d: d.find_element(By.ID, "organization").is_enabled())

        organization_input = wait.until(EC.element_to_be_clickable((By.ID, "organization")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", organization_input)
        time.sleep(0.5)
        organization_input.click()
        time.sleep(0.5)
        organization_input.clear()
        organization_input.send_keys("WORD Wrocław")
        time.sleep(0.5)
        organization_input.send_keys(Keys.ENTER)
        time.sleep(0.5)

        next_button = wait.until(EC.element_to_be_clickable((By.ID, "next-btn")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button)
        time.sleep(0.5)
        next_button.click()
        time.sleep(1)

        wait.until(EC.presence_of_element_located((By.ID, "practical-container")))
        practice_radio = driver.find_element(By.ID, "practical-container")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", practice_radio)
        practice_radio.click()
        time.sleep(0.5)

        # Починаємо перевірку дат
        buttons = driver.find_elements(By.XPATH, "//button[.//div[contains(text(), 'Wybierz')]]")

        date_found = False

        for btn in buttons:
            try:
                parent = btn.find_element(By.XPATH, "./ancestor::div[contains(@class, 'exam-date') or contains(@class, 'ng-star-inserted')]")
                date_h5 = parent.find_element(By.XPATH, ".//h5[contains(@class, 'm-0')]")
                
                text = date_h5.text.strip()
                parts = text.split()
                if len(parts) < 2:
                    continue
                day_month = parts[1]
                full_date_str = f"{day_month}.2025"
                date_obj = datetime.strptime(full_date_str, "%d.%m.%Y")

                if date_obj <= TARGET_DATE:
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
                    time.sleep(1)
                    btn.click()
                    print(f"✅ Обрано дату: {full_date_str}")
                    date_found = True
                    break
        
            except Exception as e:
                print(f"⚠️ Проблема з кнопкою: {e}")

        if not date_found:
            print("❌ Дата не знайдена, перезапускаємо перевірку...")
            raise Exception("Дата не знайдена")

        next_button = wait.until(EC.element_to_be_clickable((By.ID, "confirm-modal-btn")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button)
        time.sleep(0.5)
        next_button.click()
        time.sleep(0.5)

        next_button = wait.until(EC.element_to_be_clickable((By.ID, "next-btn")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button)
        time.sleep(0.5)
        next_button.click()
        time.sleep(1)

        potwierdzam_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//div[contains(text(), 'Potwierdzam')]]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", potwierdzam_btn)
        time.sleep(0.5)
        potwierdzam_btn.click()
        print("✅ Кнопка 'Potwierdzam' натиснута. Очікую 10 хвилин для оплати...")

        time.sleep(600)  # 10 хвилин

    except Exception as e:
        print("❌ Помилка:", e)
        raise  # щоб у головному циклі відловити і перезапустити

    finally:
        driver.quit()

if __name__ == "__main__":
    while True:
        try:
            print("🔄 Перевірка...")
            run_checker()
        except Exception as e:
            print(f"❗️ Помилка чи дата не знайдена: {e}")
            print("⏳ Чекаємо 1 хвилину і перезапускаємо...")
            time.sleep(1)
        else:
            print("⏳ Чекаємо 5 хвилин до наступної перевірки...")
            time.sleep(300)
