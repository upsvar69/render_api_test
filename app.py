from flask import Flask
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

DUCKDUCKGO_SEARCH_URL = "https://html.duckduckgo.com/html/"
QUERY = '"Belt and Road Initiative"'


@app.route("/")
def home():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    }
    debug_log = []
    articles = []

    try:
        debug_log.append("🔍 Sending POST request to DuckDuckGo...")
        response = requests.post(DUCKDUCKGO_SEARCH_URL, data={'q': QUERY}, headers=headers, timeout=10)
        debug_log.append(f"📡 DuckDuckGo response status: {response.status_code}")
        debug_log.append(f"📦 Content size: {len(response.content)} bytes")

        soup = BeautifulSoup(response.text, "html.parser")

        result_blocks = soup.select("a.result__a")
        debug_log.append(f"🔍 Found {len(result_blocks)} result links")

        for idx, a in enumerate(result_blocks[:10]):  # Only take first 10
            title = a.get_text(strip=True)
            link = a.get('href')

            debug_log.append(f"   ✅ Found article: {title} ({link})")
            articles.append((title, link))

        html = "<h1>🔗 Articles on Belt and Road Initiative (via DuckDuckGo)</h1><ul>"
        for title, link in articles:
            html += f'<li><a href="{link}" target="_blank">{title}</a></li>'
        html += "</ul>"

        html += "<hr><h2>🧪 Debug Info</h2><pre>" + "\n".join(debug_log) + "</pre>"
        html += "<h3>Sample raw HTML (first 500 chars)</h3><pre>" + response.text[:500].replace("<", "&lt;") + "</pre>"

        return html

    except Exception as e:
        debug_text = "\n".join(debug_log)
        return f"<h1>❌ Error</h1><pre>{e}</pre><hr><pre>{debug_text}</pre>"