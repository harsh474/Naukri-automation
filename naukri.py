from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys 
from Connect_tutorial_sheet import add_row_in_sheet
import time

# Update with your credentials
EMAIL = "harshrajput1101@gmail.com"
PASSWORD = "vDX9#qK8K.uvY4f"
JOB_URL = "https://www.naukri.com/react-dot-js-react-developer-jobs?k=react.js%2C%20react%20developer&nignbevent_src=jobsearchDeskGNB&experience=1&jobAge=1&functionAreaIdGid=5&ctcFilter=6to10&glbl_qcrc=1028"

# Setup Chrome Driver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
# driver = webdriver.Chrome(service=Service("chromedriver"), options=options)
driver = webdriver.Chrome(service=Service("/usr/local/bin/chromedriver"), options=options)

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

        try:
            apply_button = driver.find_element(By.XPATH, "//button[contains(text(),'Apply')]") 
            if "apply on company site" in page_text.lower() or popup_found:
                    write_to_google_sheet(job_link, company_name, today_date)
                    close_tab()
            
            apply_button.click()
            time.sleep(4)
            
            # Detect if question popup appeared
            if len(driver.find_elements(By.CLASS_NAME, "qna-title")) > 0:
                print("Question popup found. Closing tab.")
            else:
                print("Applied successfully.")
        except:
            print("No apply button or already applied.")

    except Exception as e:
        print("Error:", e)

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

def main():
    login_naukri()
    links = scrape_job_links()
    for i, link in enumerate(links):
        print(f"--- Job {i+1} of {len(links)} ---")
        apply_to_job(link)
        time.sleep(2)

    print("All jobs processed.")
    driver.quit()

if __name__ == "__main__":
    main()
