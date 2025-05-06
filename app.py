from flask import Flask
import requests
from bs4 import BeautifulSoup
from newspaper import Article
import time
import traceback

app = Flask(__name__)

DUCKDUCKGO_SEARCH_URL = "https://html.duckduckgo.com/html/"
SEARCH_QUERY = '"Belt and Road Initiative"'
MAX_ARTICLES = 10

@app.route("/")
def home():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    }
    debug_log = []
    results_html = "<h1>🔗 Articles on Belt and Road Initiative (via DuckDuckGo)</h1><ul>"
    article_count = 0

    try:
        debug_log.append("🔍 Sending POST request to DuckDuckGo...")
        response = requests.post(DUCKDUCKGO_SEARCH_URL, data={'q': SEARCH_QUERY}, headers=headers, timeout=10)
        debug_log.append(f"📡 DuckDuckGo response status: {response.status_code}")
        debug_log.append(f"📦 Content size: {len(response.content)} bytes")

        soup = BeautifulSoup(response.text, "html.parser")
        result_links = soup.select("a.result__a")
        debug_log.append(f"🔍 Found {len(result_links)} result links")

        for a in result_links:
            if article_count >= MAX_ARTICLES:
                break

            raw_title = a.get_text(strip=True)
            link = a.get('href')
            debug_log.append(f"🔗 Processing link: {raw_title} ({link})")

            try:
                article = Article(link)
                article.download()
                article.parse()

                article_title = article.title or raw_title or "No Title"
                authors = ', '.join(article.authors) or "Unknown Author"
                source = article.source_url or "Unknown Source"
                text_snippet = article.text[:500].replace("\n", " ") + "..."

                results_html += f"""
                    <li>
                        <strong>Title:</strong> <a href="{link}" target="_blank">{article_title}</a><br>
                        <strong>Author(s):</strong> {authors}<br>
                        <strong>Source:</strong> {source}<br>
                        <strong>Excerpt:</strong> {text_snippet}
                    </li><hr>
                """
                debug_log.append(f"✅ Successfully extracted article: {article_title}")
            except Exception as e:
                debug_log.append(f"❌ Failed to extract article content: {link}")
                debug_log.append(f"   Error: {str(e)}")
                results_html += f"""
                    <li>
                        <strong>Title:</strong> <a href="{link}" target="_blank">{raw_title}</a><br>
                        <strong>Status:</strong> Could not extract full article details.
                    </li><hr>
                """

            article_count += 1
            time.sleep(1)  # Be polite: wait 1 second between processing each article

        results_html += "</ul>"

    except Exception as e:
        debug_log.append(f"❌ Critical error: {str(e)}")
        debug_log.append(traceback.format_exc())
        results_html = "<h1>❌ Error during processing</h1>"

    debug_html = "<hr><h2>🧪 Debug Info</h2><pre>" + "\n".join(debug_log) + "</pre>"
    return results_html + debug_html