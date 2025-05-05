"""
We couldnt hook up chrome to the render.com
we solved this problem through cordel22 but was useless
cause google wont let u scrape with selenium anyway
next step is modigy the working beautiful soup scraper on google
to duckduck go and see if we can get the data
"""

from flask import Flask
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import selenium
import os

app = Flask(__name__)

@app.route('/')
def scrape_google():
    print(f"🧩 Selenium version: {selenium.__version__}")

    # Use environment variables for Chrome and Chromedriver paths
    chrome_path = os.environ.get("CHROME_BIN", "/usr/bin/chromium-browser")
    driver_path = os.environ.get("CHROMEDRIVER_PATH", "/usr/bin/chromedriver")

    print(f"🔍 Checking Chrome binary path: {chrome_path}")
    print(f"🔍 Checking Chromedriver path: {driver_path}")
    print(f"🔍 Chrome exists: {os.path.exists(chrome_path)}")
    print(f"🔍 Chromedriver exists: {os.path.exists(driver_path)}")

    if not os.path.exists(chrome_path):
        print("⚠️ Chrome binary not found at expected path.")
        return {"error": "Chrome binary not found."}
    if not os.path.exists(driver_path):
        print("⚠️ Chromedriver not found at expected path.")
        return {"error": "Chromedriver not found."}

    try:
        options = webdriver.ChromeOptions()
        options.binary_location = chrome_path
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        print("🚀 Launching Chrome browser...")
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=options)

        query = "Belt and Road Initiative"
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        print(f"🌐 Navigating to: {search_url}")

        driver.get(search_url)
        time.sleep(3)

        print("🔎 Scraping links...")
        results = driver.find_elements(By.CSS_SELECTOR, 'div.yuRUbf > a')
        links = [a.get_attribute('href') for a in results]

        print(f"✅ Found {len(links)} links.")
        for link in links:
            print(link)

        driver.quit()
        return {"links": links}

    except Exception as e:
        print(f"❌ Exception occurred: {str(e)}")
        return {"error": str(e)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
