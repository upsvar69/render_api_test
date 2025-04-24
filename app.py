from flask import Flask
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

BBC_SEARCH_URL = "https://www.bbc.co.uk/search?q=Belt+and+Road+Initiative"

@app.route("/")
def home():
    debug_log = []

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(BBC_SEARCH_URL, headers=headers, timeout=10)

        status_code = response.status_code
        content_length = len(response.content)
        raw_html = response.text[:1000]

        soup = BeautifulSoup(response.text, "html.parser")
        article_tags = soup.select("article a[href]")
        article_count = len(article_tags)

        articles = []
        for item in article_tags:
            title = item.get_text(strip=True)
            link = item["href"]
            if title and link and "www.bbc." in link:
                articles.append((title, link))
            if len(articles) >= 10:
                break

        # Build HTML output
        output = f"<h1>BBC Articles on Belt and Road Initiative</h1>"
        output += f"<p>🛰️ Status: {status_code}</p>"
        output += f"<p>📦 Content Size: {content_length} bytes</p>"
        output += f"<p>🔍 Links Found: {article_count}</p>"
        output += "<ul>"
        for title, link in articles:
            output += f'<li><a href="{link}" target="_blank">{title}</a></li>'
        output += "</ul>"

        output += "<hr><h2>🧪 Debug Info</h2>"
        output += "<pre>" + raw_html + "</pre>"

        return output

    except Exception as e:
        return f"<h1>❌ Error</h1><pre>{e}</pre>"