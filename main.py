import os
import time
import threading
from flask import Flask
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)

# Configuration
USERNAME = os.environ.get("LEME_EMAIL")
PASSWORD = os.environ.get("LEME_PASSWORD")
SERVER_URL = "https://lemehost.com/server/10079641/free-plan"
LOGIN_URL = "https://lemehost.com/site/login"

def run_extension():
    while True:
        print("\n--- STARTING NEW CYCLE ---")
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        # Pretend to be a real browser to avoid bot detection
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 30)

        try:
            # 1. STEP: LOGIN
            print(f"DEBUG: Navigating to {LOGIN_URL}")
            driver.get(LOGIN_URL)
            print(f"DEBUG: Current Page Title: {driver.title}")

            print("DEBUG: Looking for login fields...")
            # Lemehost uses 'LoginForm[email]' and 'LoginForm[password]'
            email_field = wait.until(EC.presence_of_element_located((By.NAME, "LoginForm[email]")))
            pass_field = driver.find_element(By.NAME, "LoginForm[password]")
            
            email_field.send_keys(USERNAME)
            pass_field.send_keys(PASSWORD)
            
            print("DEBUG: Clicking login button...")
            driver.find_element(By.NAME, "login-button").click()
            
            # Wait for redirect
            time.sleep(5)
            print(f"DEBUG: After login URL: {driver.current_url}")

            # 2. STEP: GO TO SERVER PAGE
            print(f"DEBUG: Navigating to server page: {SERVER_URL}")
            driver.get(SERVER_URL)
            time.sleep(3)
            print(f"DEBUG: Server Page Title: {driver.title}")

            # 3. STEP: FIND AND CLICK EXTEND
            print("DEBUG: Searching for the 'Extend time' button...")
            # This XPath looks for a button that contains the text 'Extend time'
            extend_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(., 'Extend time')]")
            ))
            
            print("DEBUG: Button found! Clicking now...")
            # Use JavaScript to click just in case the button is covered by a popup
            driver.execute_script("arguments[0].click();", extend_button)
            
            print("SUCCESS: Click command sent to the button.")
            
            # Final check
            time.sleep(5)
            print(f"DEBUG: Final URL after click: {driver.current_url}")

        except Exception as e:
            print(f"ERROR during automation: {str(e)}")
            # This will print the first 500 characters of the page source if it fails
            # so you can see if there was a Captcha or Error message.
            print("DEBUG: Page snippet at time of error:")
            print(driver.page_source[:500])
        finally:
            driver.quit()
        
        print("--- CYCLE FINISHED. Sleeping 20 mins ---")
        time.sleep(1200)

@app.route('/')
def home():
    return "Auto-Clicker is Running!"

if __name__ == "__main__":
    threading.Thread(target=run_extension, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
