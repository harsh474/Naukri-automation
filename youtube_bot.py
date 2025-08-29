import time
import pickle
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Your credentials
EMAIL = "harshrajput1101@gmail.com"
PASSWORD = "vDX9#qK8K.uvY4f"
COOKIE_FILE = "naukri_cookies.pkl"

# Setup Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def save_cookies():
    with open(COOKIE_FILE, "wb") as f:
        pickle.dump(driver.get_cookies(), f)
    print("Cookies saved ✅")

def load_cookies():
    with open(COOKIE_FILE, "rb") as f:
        cookies = pickle.load(f)
        for cookie in cookies:
            driver.add_cookie(cookie)
    print("Cookies loaded ✅")

def login_naukri():
    driver.get("https://www.naukri.com/mnjuser/login")
    time.sleep(3)

    email_input = driver.find_element(By.ID, "usernameField")
    password_input = driver.find_element(By.ID, "passwordField")

    email_input.send_keys(EMAIL)
    password_input.send_keys(PASSWORD)
    driver.find_element(By.XPATH, "//button[text()='Login']").click()
    time.sleep(5)
    print("Logged in with username/password ✅")

if __name__ == "__main__":
    driver.get("https://www.naukri.com/mnjuser/login")
    time.sleep(3)

    # Check if cookie file exists
    if os.path.exists(COOKIE_FILE):
        try:
            load_cookies()
            driver.get("https://www.naukri.com/mnjuser/homepage")  # direct dashboard
            time.sleep(5)
            print("Logged in using cookies ✅")
        except Exception as e:
            print("Error loading cookies, fallback to login:", e)
            login_naukri()
            save_cookies()
    else:
        # First time login
        login_naukri()
        save_cookies()
