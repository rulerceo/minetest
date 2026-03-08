import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuration - Use Environment Variables for Security
USERNAME = os.environ.get("LEME_EMAIL", "vishwasr235@gmail.com")
PASSWORD = os.environ.get("LEME_PASSWORD", "Vishwasr@2009")
SERVER_URL = "https://lemehost.com/server/10079641/free-plan"
LOGIN_URL = "https://lemehost.com/site/login"

def run_extension():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Required for Render
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 20)

    try:
        print("Logging in...")
        driver.get(LOGIN_URL)
        
        # Fill login form (Adjust selectors if IDs are different)
        wait.until(EC.presence_of_element_located((By.NAME, "LoginForm[email]"))).send_keys(USERNAME)
        driver.find_element(By.NAME, "LoginForm[password]").send_keys(PASSWORD)
        
        # Click Login Button
        driver.find_element(By.NAME, "login-button").click()
        time.sleep(3) # Wait for redirect

        print(f"Navigating to {SERVER_URL}...")
        driver.get(SERVER_URL)

        # Target the 'Extend time' button specifically
        extend_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(), 'Extend time')]")
        ))
        
        extend_button.click()
        print("Button clicked successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    while True:
        run_extension()
        print("Waiting 20 minutes for next run...")
        time.sleep(1200) # 20 minutes in seconds
