from flask import Flask
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import time


app = Flask(__name__)

SEARCH_QUERY = 'site:bbc.com "Belt and Road Initiative"'
GOOGLE_SEARCH_URL = f"https://www.google.com/search?q={SEARCH_QUERY.replace(' ', '+')}"

@app.route("/")
def home():
    debug_log = ["🔍 Launching headless Chrome..."]
    import subprocess
    debug_log.append("📝 Installed binaries:\n" + subprocess.getoutput("ls -la /usr/bin | grep chrome"))
    articles = []

    try:
        # Setup Chrome options for headless operation in containers
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0")
        
        # Explicitly set binary location
        chrome_options.binary_location = "/usr/bin/google-chrome"

        # Initialize Chrome with webdriver_manager
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )

        debug_log.append("🌐 Navigating to Google...")
        driver.get(GOOGLE_SEARCH_URL)
        time.sleep(3)  # Wait for JavaScript to load content

        results = driver.find_elements(By.CSS_SELECTOR, "div.yuRUbf a[href]")
        debug_log.append(f"🔍 Found {len(results)} results.")

        for idx, a_tag in enumerate(results[:10]):
            try:
                title_element = a_tag.find_element(By.TAG_NAME, "h3")
                title = title_element.text.strip()
                url = a_tag.get_attribute("href")

                if "bbc.com" in url:
                    articles.append((title, url))
                    debug_log.append(f"   ✅ #{idx + 1}: {title}")
                else:
                    debug_log.append(f"   ⚠️ Skipping non-BBC link: {url}")
            except:
                debug_log.append(f"   ❌ No <h3> found in result #{idx + 1}")
                continue

        driver.quit()

        # Build HTML response
        html = "<h1>🔗 BBC Articles on Belt and Road Initiative (via Google + Selenium)</h1><ul>"
        for title, url in articles:
            html += f'<li><a href="{url}" target="_blank">{title}</a></li>'
        html += "</ul>"

        html += "<hr><h2>🧪 Debug Info</h2><pre>" + "\n".join(debug_log) + "</pre>"
        return html

    except Exception as e:
        debug_log.append(f"❌ Exception occurred: {e}")
        debug_text = "\n".join(debug_log)
        return f"<h1>❌ Error</h1><pre>{e}</pre><hr><pre>{debug_text}</pre>"

if __name__ == "__main__":
    app.run(debug=True)