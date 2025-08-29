from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys  
from database.insert_operation import insert_employee
from webdriver_manager.chrome import ChromeDriverManager
import time 
import pickle
import os
import json


# Credentials
# EMAIL = "2020kuec2050@iiitkota.ac.in"
EMAIL = "harshrajput1101@gmail.com"
# PASSWORD = "123@#abC$"
PASSWORD = "HAR@Sh1101"
LINKEDIN_URL="https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin"

# Setup Chrome Driver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
# driver = webdriver.Chrome(service=Service("/usr/local/bin/chromedriver"), options=options)
COOKIE_FILE = "linkedin_cookies.pkl"

# Setup Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def save_cookies():
        with open(COOKIE_FILE, "wb") as f:
         pickle.dump(driver.get_cookies(), f)
        print("Cookies saved ✅")

def load_cookies():
    try:
        with open(COOKIE_FILE, "rb") as f:   # binary mode hi use karna
            cookies = pickle.load(f)
            for cookie in cookies:
                driver.add_cookie(cookie) 

        driver.get('https://www.linkedin.com/feed/')
        print("Cookies loaded ✅")
        return True
    except FileNotFoundError:
        print("No cookie file found")
        return False
    except Exception as e:
        print("Error loading cookies:", e)
        return False

def login_linkedin():
    print("Logging in...") 
    driver.get(LINKEDIN_URL)
    time.sleep(3)

    email_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")

    email_input.send_keys(EMAIL)
    password_input.send_keys(PASSWORD)
    driver.find_element(By.XPATH, "//button[normalize-space()='Sign in']").click()
    time.sleep(5)
    print("Logged in successfully.")

def search_people(company="Google"):
         # Search for company
    search_element = driver.find_element(By.XPATH, "//input[@placeholder='Search']") 
    print("search_element",search_element)
    search_element.send_keys(company)
    search_element.send_keys(Keys.RETURN)
    time.sleep(10)

    # Click People filter
    people_filter = driver.find_element(By.XPATH, "//button[@aria-pressed='false'][normalize-space()='People']")
    people_filter.click()
    time.sleep(10)

    # Click 1st connection filter
    first_filter = driver.find_element(By.XPATH, "//button[normalize-space()='1st']")
    first_filter.click()
    time.sleep(10)

    # Select first 5 <li> from main UL 
    try :
        people_cards = driver.find_elements(
            By.CSS_SELECTOR, ".nrAZYpTYFusNwfgyknMGSmTcNDvoxKyKg li"
        )[:5]
        print("people_cards",people_cards)
    except Exception as e:
        print("error while finding people",e)

    employee_data = []

    for card in people_cards:
        try:
            # get anchor (profile link) 
            print("card",card);
            link_element = card.find_element(By.CSS_SELECTOR, "a")
            profile_url = link_element.get_attribute("href")

            # get name inside span[aria-hidden="true"]
            name_element = card.find_element(By.CSS_SELECTOR, "span[aria-hidden='true']")
            name = name_element.text.strip()

            employee_data.append({"name": name, "url": profile_url})
        except Exception as e:
            print("Error extracting data:", e)

    print("employee_data:", employee_data)
    return employee_data


def main(): 
    company = "Cred"
    driver.get(LINKEDIN_URL)
    time.sleep(5)
    if os.path.exists(COOKIE_FILE):
            try:
                driver.get(LINKEDIN_URL)   # Pehle site kholni zaruri hai
                load_cookies()
                print("Logged in using cookies ✅")
            except Exception as e:
                print("Error loading cookies, fallback to login:", e)
                # login_linkedin()
                # save_cookies()
    else:
        # First time login
        login_linkedin()
        save_cookies()

    employees = search_people(company)
    print("\nTop 5 Employee LinkedIn URLs:") 
    insert_employee(employees,company) 
    for u in employees:
        print(u) 
    time.sleep(12)
    driver.quit()


if __name__ == "__main__":
    main() 
   


# dUpFNQejEIgGUgMCsAZivCDPnWDziPVjOsw 
# main container_class = "nrAZYpTYFusNwfgyknMGSmTcNDvoxKyKg"
# li_class="dUpFNQejEIgGUgMCsAZivCDPnWDziPVjOsw" 





