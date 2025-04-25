"""
You’re pulling search results from Google using requests + BeautifulSoup, but we know this breaks down if results are heavily JS-rendered or if Google decides to serve a script-first version (which it does more often now).
"""



from flask import Flask
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

GOOGLE_SEARCH_URL = "https://www.google.com/search?q=site:bbc.com+%22Belt+and+Road+Initiative%22"

@app.route("/")
def home():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    }

    debug_log = []
    articles = []

    try:
        debug_log.append("🔍 Sending request to Google search...")
        response = requests.get(GOOGLE_SEARCH_URL, headers=headers, timeout=10)
        debug_log.append(f"📡 Google response status: {response.status_code}")
        debug_log.append(f"📦 Content size: {len(response.content)} bytes")

        soup = BeautifulSoup(response.text, "html.parser")

        result_blocks = soup.select("div.yuRUbf a[href]")
        debug_log.append(f"🔍 Found {len(result_blocks)} <a> tags inside div.yuRUbf")

        found_titles = 0
        for idx, a in enumerate(result_blocks):
            debug_log.append(f"🔗 Checking link #{idx + 1}")
            title_tag = a.find("h3")
            if not title_tag:
                debug_log.append("   ❌ No <h3> tag inside <a>")
                continue

            title = title_tag.get_text(strip=True)
            link = a.get("href")

            if "bbc.com" not in link:
                debug_log.append(f"   ⚠️ Link does not point to bbc.com: {link}")
                continue

            debug_log.append(f"   ✅ Found BBC article: {title}")
            articles.append((title, link))
            found_titles += 1

            if found_titles >= 10:
                break

        html = "<h1>🔗 BBC Articles on Belt and Road Initiative Again (via Google)</h1><ul>"
        for title, link in articles:
            html += f'<li><a href="{link}" target="_blank">{title}</a></li>'
        html += "</ul>"

        html += "<hr><h2>🧪 Debug Info</h2><pre>" + "\n".join(debug_log) + "</pre>"
        html += "<h3>Sample raw HTML (first 500 chars)</h3><pre>" + response.text[:500].replace("<", "&lt;") + "</pre>"

        return html

    except Exception as e:
        debug_text = "\n".join(debug_log)
        return f"<h1>❌ Error</h1><pre>{e}</pre><hr><pre>{debug_text}</pre>"