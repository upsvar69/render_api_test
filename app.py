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

        # Match the real Google structure
        result_blocks = soup.select("div.yuRUbf a[href]")

        for a in result_blocks:
            title_tag = a.find("h3")
            if title_tag and "bbc.com" in a["href"]:
                title = title_tag.get_text(strip=True)
                link = a["href"]
                articles.append((title, link))
            if len(articles) >= 10:
                break

        html = "<h1>🔗 BBC Articles on Belt and Road Initiative Again(via Google)</h1><ul>"
        for title, link in articles:
            html += f'<li><a href="{link}" target="_blank">{title}</a></li>'
        html += "</ul>"

        html += "<hr><h2>🧪 Debug Info</h2><pre>" + "\n".join(debug_log) + "</pre>"
        html += "<h3>Sample raw HTML (first 500 chars)</h3><pre>" + response.text[:500] + "</pre>"

        return html

    except Exception as e:
        return f"<h1>❌ Error</h1><pre>{e}</pre><hr><pre>{'\n'.join(debug_log)}</pre>"