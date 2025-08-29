from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys 
from database.insert_operation import insert_job_profile  
from webdriver_manager.chrome import ChromeDriverManager
import time 
import pickle
import os
# Update with your credentials
EMAIL = "harshrajput1101@gmail.com"
PASSWORD = "vDX9#qK8K.uvY4f"
JOB_URL = "https://www.naukri.com/react-dot-js-react-developer-jobs?k=react.js%2C%20react%20developer&nignbevent_src=jobsearchDeskGNB&experience=1&jobAge=1&functionAreaIdGid=5&ctcFilter=6to10&glbl_qcrc=1028"
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
    print("Logging in...")
    driver.get("https://www.naukri.com/mnjuser/login")
    time.sleep(3)

    email_input = driver.find_element(By.ID, "usernameField")
    password_input = driver.find_element(By.ID, "passwordField")

    email_input.send_keys(EMAIL)
    password_input.send_keys(PASSWORD)
    driver.find_element(By.XPATH, "//button[text()='Login']").click()
    time.sleep(5)
    print("Logged in successfully.")

def scrape_job_links():
    print("Scraping jobs...")
    driver.get(JOB_URL)
    time.sleep(5)
    job_links = []
    job_cards = driver.find_elements(By.CSS_SELECTOR, "a.title")
    for card in job_cards:
        link = card.get_attribute("href")
        if link:
            job_links.append(link)
    print(f"Found {len(job_links)} jobs.")
    return job_links

def apply_to_job(link): 
    try:
        print(f"Applying to job: {link}")
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(link)
        time.sleep(4) 

        # ✅ Fetch job role
        try:
            job_profile_element = driver.find_element(By.CLASS_NAME, "styles_jd-header-title__rZwM1") 
            job_role = job_profile_element.text
            print("job_profile_element", job_role)
        except:
            job_role = "N/A"

        # ✅ Fetch company name
        try:
            company_element = driver.find_element(By.CLASS_NAME, "styles_jd-header-comp-name__MvqAI")
            company_name = company_element.text
            print("company_name", company_name)
        except:
            company_name = "N/A"

        try:
            apply_button = driver.find_elements(By.ID, "apply-button")
            apply_button = apply_button[0] if apply_button else None

            if apply_button:
                apply_button.click()
                time.sleep(7)
                insert_job_profile(company_name, job_role, "NA", "Need to found")

                if len(driver.find_elements(By.CLASS_NAME, "qna-title")) > 0:
                    print("Question popup found. Closing tab.")
                else:
                    print("Applied successfully.") 

            else:
                print("We have to apply on company site")
                company_button_site = driver.find_element(By.ID, "company-site-button")

                original_window_handle = driver.current_window_handle
                before_tabs = driver.window_handles

                company_button_site.click()
                time.sleep(5)

                after_tabs = driver.window_handles
                new_tabs = list(set(after_tabs) - set(before_tabs))
                new_tab = new_tabs[0] if new_tabs else None

                if new_tab:
                    driver.switch_to.window(new_tab)
                    time.sleep(3)
                    career_page_link = driver.current_url
                    print("Company site link:", career_page_link)

                    insert_job_profile(company_name, job_role, career_page_link, "Available")

                    # ✅ Close company site tab and return
                    driver.close()
                    driver.switch_to.window(original_window_handle)
                else:
                    print("❌ No new tab opened for company site.")

        except Exception as e:
            print("Error while applying:", e)

    except Exception as e:
        print("Error:", e)

    # ✅ Always close the job detail tab and go back to main
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

def main():
    # login_naukri() 
    driver.get("https://www.naukri.com/mnjuser/login")
    time.sleep(5)

    # Check if cookie file exists
    if os.path.exists(COOKIE_FILE):
        try:
            load_cookies()
            # driver.get("https://www.naukri.com/mnjuser/homepage")  # direct dashboard
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


        
    links = scrape_job_links()
    
    for i, link in enumerate(links):
        print(f"--- Job {i+1} of {len(links)} ---")
        apply_to_job(link)
        time.sleep(2)

    print("All jobs processed.")
    driver.quit()

if __name__ == "__main__":
    main()



# Setup Chrome Driver
# options = webdriver.ChromeOptions()
# options.add_argument("--start-maximized")
# # driver = webdriver.Chrome(service=Service("chromedriver"), options=options)
# # driver = webdriver.Chrome(service=Service("/usr/local/bin/chromedriver"), options=options) 
