from flask import Flask, render_template_string
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

BBC_SEARCH_URL = "https://www.bbc.co.uk/search?q=Belt+and+Road+Initiative"

@app.route("/")
def home():
    try:
        # Get search results page
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(BBC_SEARCH_URL, headers=headers, timeout=10)
        response.raise_for_status()

        # Parse HTML
        soup = BeautifulSoup(response.text, "html.parser")
        articles = []

        # Find article links and titles
        for item in soup.select("article a[href]"):
            title = item.get_text(strip=True)
            link = item["href"]
            if title and link and "www.bbc." in link:
                articles.append((title, link))
            if len(articles) >= 10:
                break

        # Render basic HTML with articles
        html = "<h1>BBC Articles on Belt and Road Initiative</h1><ul>"
        for title, link in articles:
            html += f'<li><a href="{link}" target="_blank">{title}</a></li>'
        html += "</ul>"

        return html

    except Exception as e:
        return f"<h1>Error fetching articles</h1><p>{e}</p>"

