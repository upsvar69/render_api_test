from flask import Flask, render_template_string
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

BBC_SEARCH_URL = "https://www.bbc.co.uk/search?q=Belt+and+Road+Initiative"

@app.route("/")
def home():
    debug_log = []

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        debug_log.append(f"🔍 Sending request to BBC Search URL: {BBC_SEARCH_URL}")
        response = requests.get(BBC_SEARCH_URL, headers=headers, timeout=10)

        debug_log.append(f"📡 Response status: {response.status_code}")
        debug_log.append(f"📦 Content size: {len(response.content)} bytes")

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        articles = []
        for item in soup.select("article a[href]"):
            title = item.get_text(strip=True)
            link = item["href"]
            if title and link and "www.bbc." in link:
                articles.append((title, link))
            if len(articles) >= 10:
                break

        debug_log.append(f"📰 Articles found: {len(articles)}")

        html = "<h1>BBC Articles on Belt and Road Initiative</h1><ul>"
        for title, link in articles:
            html += f'<li><a href="{link}" target="_blank">{title}</a></li>'
        html += "</ul><hr>"

        # Add debug section
        html += "<h2>Debug Info</h2><pre>" + "\n".join(debug_log) + "</pre>"
        html += "<h3>Sample of raw HTML response (first 500 chars)</h3><pre>" + response.text[:500] + "</pre>"

        return html

    except requests.exceptions.RequestException as req_err:
        return f"<h1>❌ Network error</h1><pre>{req_err}</pre><hr><pre>{'\n'.join(debug_log)}</pre>"

    except Exception as e:
        return f"<h1>❌ General error</h1><pre>{e}</pre><hr><pre>{'\n'.join(debug_log)}</pre>"
