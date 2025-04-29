from flask import Flask
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import selenium
import os
import subprocess

app = Flask(__name__)

def find_chrome():
    try:
        # Use `find` to search for chrome binary in the cache
        result = subprocess.run(
            ["find", "/opt/render/project/.render", "-type", "f", "-name", "google-chrome"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        path = result.stdout.strip()
        if path:
            print(f"🔍 Chrome binary found at: {path}")
            return path
        else:
            print("⚠️ Chrome binary not found using grep/find.")
            return None
    except Exception as e:
        print(f"❌ Error while searching for Chrome: {e}")
        return None

@app.route('/')
def scrape_google():
    print(f"🧩 Selenium version: {selenium.__version__}")

    chrome_path = "/opt/render/project/.render/chrome/opt/google/chrome/google-chrome"
    if not os.path.isfile(chrome_path):
        chrome_path = find_chrome()
        if not chrome_path:
            return {"error": "Chrome binary not found."}

    try:
        options = webdriver.ChromeOptions()
        options.binary_location = chrome_path
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        print("🚀 Launching Chrome browser...")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

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