from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time



def send_adobe_sign(template_name, user_email):
 
    # options.add_argument("--headless")  # For production
    driver = webdriver.Chrome()

    try:
        # Step 1.1 – Open login page
        driver.get("https://na1.documents.adobe.com/public/compose")
        time.sleep(2)

        # Step 1.2 – Enter email
        email_input = driver.find_element(By.XPATH, "//input[@id='EmailPage-EmailField']")
        email_input.send_keys("jcullenre@gmail.com")
        time.sleep(1)

        # Step 1.2 – Click continue (button XPath needed)
        continue_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
        continue_btn.click()
        time.sleep(3)

        # Step 1.3 – Click “Choose a different method to verify”
        driver.find_element(By.XPATH, "//a[normalize-space()='Choose a different method to verify']").click()
        time.sleep(2)

        # Step 1.4 – Click “Confirm your phone number ending in -15”
        driver.find_element(By.XPATH, "//div[2]//div[1]//div[1]//div[1]//div[2]//div[1]//div[1]").click()
        time.sleep(1)
         
        digit_inputs = driver.find_elements(By.XPATH, "//input[@type='number']")
        digit_inputs[0].send_keys("4")
        digit_inputs[1].send_keys("5")
        # Step 1.5 – Enter 2-digit code: 4, 5
        # digit1 = driver.find_element(By.XPATH, "//input[@id='react-aria2856568547-80']")
        # digit2 = driver.find_element(By.XPATH, "//input[@id='react-aria2856568547-86']")
        # digit1.send_keys("4")
        # digit2.send_keys("5")
        time.sleep(2)

        # Step 1.6 – Click continue
        driver.find_element(By.XPATH, "//button[@id='react-aria2895009630-197']").click()
        time.sleep(5)  # Wait for dashboard

        # Step 2.1 – Click "Choose File"
        driver.find_element(By.XPATH, "//button[@id='react-aria7470844299-:ra:']").click()
        time.sleep(2)

        # Step 2.2 – Click "Templates" tab
        driver.find_element(By.XPATH, "//span[@class='FzVSrW_spectrum-Tabs-itemLabel'][normalize-space()='Templates']").click()
        time.sleep(2)

        # Step 2.3 – Search for template
        search_input = driver.find_element(By.XPATH, "//input[@id='react-aria7470844299-:r9i:']")
        search_input.send_keys(template_name)
        time.sleep(2)

        # Step 2.4 – Select the template (assuming it's the first match)
        driver.find_element(By.XPATH, "//div[contains(@class, 'template-card')]").click()
        time.sleep(2)

        # Step 2.5 – Click continue
        driver.find_element(By.XPATH, "//span[@id='react-aria7470844299-:r8v:']").click()
        time.sleep(3)

        # Step 2.6 – Fill in recipient email
        email_field = driver.find_element(By.XPATH, "//input[@id='react-aria7470844299-:rdm:']")
        email_field.send_keys(user_email)
        time.sleep(1)

        # Step 2.7 – Click Send
        driver.find_element(By.XPATH, "//button[@id='send']").click()
        time.sleep(5)

        print("✅ Agreement sent successfully")

    except Exception as e:
        print(f"❌ Error during automation: {e}")
    finally:
        driver.quit()
        


# send_adobe_sign("ACH Vendor Payment Enrollment Form FIllable","harsh.rajput@oodles.io")


