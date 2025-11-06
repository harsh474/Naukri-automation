# run_bot.py
import os, time, pickle, base64, io, sys, json, traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from webdriver_manager.chrome import ChromeDriverManager


# --- CONFIG --- 
# mern job url
# JOB_URL = "https://www.naukri.com/react-dot-js-react-developer-jobs?k=react.js%2C%20react%20developer&nignbevent_src=jobsearchDeskGNB&experience=1&jobAge=1&functionAreaIdGid=5&ctcFilter=6to10&glbl_qcrc=1028"
# python job url
JOB_URL = "https://www.naukri.com/python-developer-django-developer-ai-ml-agent-ai-jobs?k=python%20developer%2C%20django%20developer%2C%20ai%2C%20ml%2C%20agent%20ai&nignbevent_src=jobsearchDeskGNB&experience=1&ctcFilter=6to10&ctcFilter=10to15&ctcFilter=15to25&ctcFilter=25to50&ctcFilter=50to75&ctcFilter=75to100&ctcFilter=100to500&jobAge=1"

EMAIL = os.getenv("EMAIL")              # set in GitHub Secrets
PASSWORD = os.getenv("PASSWORD")        # set in GitHub Secrets
COOKIES_B64 = os.getenv("COOKIES_B64")  # optional: base64(pickle of cookies)

# Optional: local file fallback when running locally
COOKIE_FILE = "naukri_cookies.pkl"
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def make_driver():
     opts = Options()
     # CI-safe flags
     opts.add_argument("--headless=new")
     opts.add_argument("--no-sandbox")
     opts.add_argument("--disable-dev-shm-usage")
     opts.add_argument("--window-size=1920,1080")
     # If setup-chrome sets CHROME_PATH, point Selenium to it
     chrome_bin = os.getenv("CHROME_PATH")
     if chrome_bin:
          opts.binary_location = chrome_bin

     service = Service()
     driver = webdriver.Chrome(service=service, options=opts)
     return driver



def save_cookies_pickle(driver):
    try:
        with open(COOKIE_FILE, "wb") as f:
            pickle.dump(driver.get_cookies(), f)
        print("Cookies saved to file ✅")
    except Exception:
        print("Could not save cookies to file (non-fatal)")

def load_cookies_from_b64(driver, cookies_b64):
    try:
        data = base64.b64decode(cookies_b64)
        cookies = pickle.loads(data)
        driver.get("https://www.naukri.com/")  # must be on domain before add_cookie
        for c in cookies:
            c.pop("sameSite", None)  # avoid schema mismatch
            try:
                driver.add_cookie(c)
            except Exception as e:
                print("Skipping one cookie:", e)
        print("Cookies loaded from secret ✅")
        return True
    except Exception as e:
        print("Failed to load cookies from secret:", e)
        return False

def load_cookies_from_file(driver):
    if not os.path.exists(COOKIE_FILE):
        return False
    try:
        with open(COOKIE_FILE, "rb") as f:
            cookies = pickle.load(f)
        driver.get("https://www.naukri.com/")
        for c in cookies:
            c.pop("sameSite", None)
            try:
                driver.add_cookie(c)
            except Exception as e:
                print("Skipping one cookie:", e)
        print("Cookies loaded from file ✅")
        return True
    except Exception as e:
        print("Failed to load cookies from file:", e)
        return False

def login_naukri(driver):
    print("Logging in…")
    driver.get("https://www.naukri.com/mnjuser/login")
    wait = WebDriverWait(driver, 20)
    email_input = wait.until(EC.visibility_of_element_located((By.ID, "usernameField")))
    password_input = wait.until(EC.visibility_of_element_located((By.ID, "passwordField")))
    email_input.clear(); email_input.send_keys(EMAIL)
    password_input.clear(); password_input.send_keys(PASSWORD)
    driver.find_element(By.XPATH, "//button[text()='Login']").click()
    wait.until(EC.url_contains("naukri.com"))  # crude success check
    print("Logged in successfully ✅")

def scrape_job_links(driver):
    print("Scraping jobs…")
    driver.get(JOB_URL)
    WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.title")))
    cards = driver.find_elements(By.CSS_SELECTOR, "a.title")
    links = []
    for card in cards:
        href = card.get_attribute("href")
        if href:
            links.append(href)
    print(f"Found {len(links)} jobs.")
    return links

def apply_to_job(driver, link):
    try:
        print(f"Applying to job: {link}")
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(link)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # job role
        try:
            job_role = driver.find_element(By.CLASS_NAME, "styles_jd-header-title__rZwM1").get_text()
        except Exception:
            job_role = "N/A"

        # company
        try:
            company_name = driver.find_element(By.CLASS_NAME, "styles_jd-header-comp-name__MvqAI").text
        except Exception:
            company_name = "N/A"

        # try “apply” on naukri
        try:
            btns = driver.find_elements(By.ID, "apply-button")
            btn = btns[0] if btns else None
            if btn:
                btn.click()
                time.sleep(6)
                if driver.find_elements(By.CLASS_NAME, "qna-title"):
                    print("Question popup found. (treated as applied)")
                else:
                    print("Applied successfully.")
            else:
                print("No direct apply; try company site")
                company_btn = driver.find_element(By.ID, "company-site-button")
                orig = driver.current_window_handle
                before = driver.window_handles
                company_btn.click()
                time.sleep(5)
                after = driver.window_handles
                new_tabs = [t for t in after if t not in before]
                if new_tabs:
                    driver.switch_to.window(new_tabs[0])
                    time.sleep(3)
                    career_url = driver.current_url
                    print("Company site link:", career_url)
                    driver.close()
                    driver.switch_to.window(orig)
                else:
                    print("No new tab opened for company site.")
        except Exception as e:
            print("Error while applying:", e)

    except Exception as e:
        print("Error:", e)
    finally:
        # close detail tab if open
        if len(driver.window_handles) > 1:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

def main():
    # Lazy import to keep your original import path
    
     driver = make_driver()
    
     try:
          # Try cookies first (Secret → local file) then fallback to login
          got_session = False
          if COOKIES_B64:
               got_session = load_cookies_from_b64(driver, COOKIES_B64)
          if not got_session:
               got_session = load_cookies_from_file(driver)

          if not got_session:
               if not EMAIL or not PASSWORD:
                    print("No cookies and no credentials; cannot login.")
                    sys.exit(1)
               login_naukri(driver)
               save_cookies_pickle(driver)

          links = scrape_job_links(driver)
          for i, link in enumerate(links, start=1):
               print(f"--- Job {i} of {len(links)} ---")
               apply_to_job(driver, link)
               time.sleep(1)

          print("All jobs processed.")
     except Exception:
          traceback.print_exc()
          sys.exit(1)
     finally:
          driver.quit()

if __name__ == "__main__":
    main()
