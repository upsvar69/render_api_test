from flask import Flask
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import selenium

app = Flask(__name__)

@app.route('/')
def scrape_google():
    print(f"🧩 Selenium version: {selenium.__version__}")

    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Needed for Render.com
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
    app.run(host="0.0.0.0", port=8000)