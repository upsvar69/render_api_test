from flask import Flask
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
import subprocess

app = Flask(__name__)

SEARCH_QUERY = 'site:bbc.com "Belt and Road Initiative"'
GOOGLE_SEARCH_URL = f"https://www.google.com/search?q={SEARCH_QUERY.replace(' ', '+')}"

# === Utility functions ===

def find_browser_binary():
    possible_paths = [
        "/opt/render/project/.render/chrome/opt/google/chrome",  # Correct Chrome path
        "/usr/bin/google-chrome-stable",
        "/usr/bin/google-chrome",
        "/usr/bin/chromium-browser",
        "/usr/bin/chromium"
    ]
    for path in possible_paths:
        if os.path.isfile(path) and os.access(path, os.X_OK):
            return path
    return None

def log_system_info():
    """
    Collect and return useful system info for debugging.
    """
    logs = []
    logs.append("🛠️ Scanning for Chrome/Chromium binaries...")
    found_chrome_binaries = subprocess.getoutput("find / -type f -iname '*chrome*' 2>/dev/null")
    logs.append("🔎 Found Chrome-related files:\n" + found_chrome_binaries)
    usr_bin_listing = subprocess.getoutput("ls -la /usr/bin | grep chrome")
    logs.append("📄 /usr/bin Chrome entries:\n" + usr_bin_listing)
    return logs

@app.route("/")
def home():
    debug_log = []
    
    # Gather system info
    debug_log += log_system_info()

    # Find browser binary
    chrome_path = find_browser_binary()
    if not chrome_path:
        debug_log.append("❌ No Chrome or Chromium binary found!")
        chrome_path = "NOT FOUND"
    else:
        debug_log.append(f"📍 Browser binary selected: {chrome_path}")
    
    articles = []

    try:
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0")

        if chrome_path != "NOT FOUND":
            chrome_options.binary_location = chrome_path

        debug_log.append("🚀 Launching browser with Selenium...")

        # Initialize Chrome driver
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )

        debug_log.append(f"🌐 Navigating to Google search: {GOOGLE_SEARCH_URL}")
        driver.get(GOOGLE_SEARCH_URL)
        time.sleep(3)

        results = driver.find_elements(By.CSS_SELECTOR, "div.yuRUbf a[href]")
        debug_log.append(f"🔍 Found {len(results)} search results.")

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
            except Exception as e:
                debug_log.append(f"   ❌ Error processing result #{idx + 1}: {e}")

        driver.quit()

        # Build HTML response
        html = "<h1>🔗 BBC Articles on Belt and Road Initiative</h1><ul>"
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