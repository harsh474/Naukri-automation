#from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys   
from selenium.webdriver.support.ui import WebDriverWait
from database.insert_operation import insert_employee
from webdriver_manager.chrome import ChromeDriverManager
import time,pickle,os
from selenium.webdriver.support import expected_conditions as EC



# Credentials
EMAIL = "2020kuec2050@iiitkota.ac.in"
# EMAIL = "harshrajput1101@gmail.com"

# PASSWORD = "HAR@Sh1101"
LINKEDIN_URL="https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin"



#  Setup Chrome Driver
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




def open_employee_url_message():

        # step1 open this employee_linkdin_url in browswer add some dealy to load page 
        employee_linkdin_url = "https://www.linkedin.com/in/dhakad22klx/"    
        driver.get(employee_linkdin_url) 

        # WebDriverWait(driver,10)
        time.sleep(20)
        #  step2 target message button of linkdin_url  and using selector all , in return you will get array from the array extract 2nd whose index is 1 , and click on this  message button and delay to load message box 
        #  message_button_CSS_SELECTOR = ".entry-point.uAsTXlgAmXlTRIpORLsqgkfDLYJBhUwfbERWCA"  
       
 
        try: 
            # WebDriverWait(driver,10)  
            
            time.sleep(20)
            message_button_CSS_SELECTOR = ".VIyKyZZuBhznEXwJnvQbbGJYNEEmXXaayX"  
            # message_button = driver.find_elements(By.CSS_SELECTOR,message_button_CSS_SELECTOR)  
            message_button = driver.find_elements(By.XPATH,"//button[contains(@aria-label, 'Message Deepak')]")
            print("message_button is clicked",message_button) 
            print("type of message button",type(message_button)) 
            message_button[1].click() 
            time.sleep(20) 
            
    
        except Exception as e: 
            print("Print Exception as e",e)
        
        #step3 target this input element using this class name  
        try: 
            time.sleep(30)
            employee_message_box_CSS_SELECTOR = ".msg-form__contenteditable"    
            message_box_element = driver.find_elements(By.CSS_SELECTOR, employee_message_box_CSS_SELECTOR) 
            print("message_box_element",message_box_element)
    
            job_link ="https://job-boards.greenhouse.io/66degrees/jobs/5580307004"  
            employee_name = "Anil Kumar B" 

            #step4  after target, message this employee to ask for referral , 
            referral_template = f"""   
            Hello {employee_name},
            I noticed an opening at 66degrees for the Associate Software Engineer, Gradient Specialist role. My background in Python scripting, AI/ML, and data analytics aligns well with the requirements.
            I’d appreciate a referral if possible.
            {job_link}
            Thank you.
            """  


            message_box_element[0].send_keys(referral_template)
            time.sleep(4) 
            WebDriverWait(driver,4)
        except Exception as e:
            print("Error while targeting element as ",e)

        # step5 , target element with class name = "msg-form__send-button", and click on it  add delay in it 
        try:
            send_button_CSS_SELECTOR = ".msg-form__send-button"  
            send_button_element = driver.find_element(By.CSS_SELECTOR,send_button_CSS_SELECTOR)
            send_button_element.click()  
            WebDriverWait(driver,5)

        except Exception as e:
            print("error while clicking send button") 


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

    open_employee_url_message() 
    
    driver.quit()


if __name__ == "__main__":
    main() 
   

