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
        print("Starting extension cycle...")
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        
        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 20)

        try:
            driver.get(LOGIN_URL)
            wait.until(EC.presence_of_element_located((By.NAME, "LoginForm[email]"))).send_keys(USERNAME)
            driver.find_element(By.NAME, "LoginForm[password]").send_keys(PASSWORD)
            driver.find_element(By.NAME, "login-button").click()
            
            time.sleep(5)
            driver.get(SERVER_URL)
            
            # Target the button you provided
            extend_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Extend time')]")
            ))
            extend_button.click()
            print("Successfully extended!")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            driver.quit()
        
        print("Sleeping for 20 minutes...")
        time.sleep(1200)

@app.route('/')
def home():
    return "Auto-Clicker is Running!"

if __name__ == "__main__":
    # Start the clicker in a separate thread so the web server can stay active
    threading.Thread(target=run_extension, daemon=True).start()
    # Render provides the PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
