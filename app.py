from flask import Flask
from duckduckgo_search import DDGS, DuckDuckGoSearchException
from newspaper import Article
import time
import traceback

app = Flask(__name__)

SEARCH_QUERY = "Belt and Road Initiative"
MAX_ARTICLES = 10
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds

def polite_search(query, max_results):
    attempt = 0
    while attempt < MAX_RETRIES:
        try:
            with DDGS() as ddgs:
                return list(ddgs.text(query, max_results=max_results))
        except DuckDuckGoSearchException as e:
            if "Ratelimit" in str(e):
                print(f"⏳ Rate limited. Waiting {RETRY_DELAY} seconds before retrying...")
                time.sleep(RETRY_DELAY)
                attempt += 1
            else:
                raise
    raise Exception("Exceeded maximum retries for DuckDuckGo search.")

@app.route("/")
def home():
    debug_log = []
    results_html = "<h1>🔗 Articles on Belt and Road Initiative (via DuckDuckGo)</h1><ul>"
    article_count = 0

    try:
        debug_log.append("🔍 Starting polite DuckDuckGo search...")
        search_results = polite_search(SEARCH_QUERY, max_results=MAX_ARTICLES * 2)  # Ask for extra in case some fail

        for result in search_results:
            if article_count >= MAX_ARTICLES:
                break

            link = result.get('href') or result.get('url')
            if not link:
                continue

            debug_log.append(f"🔗 Processing link: {link}")
            try:
                article = Article(link)
                article.download()
                article.parse()

                title = article.title or "No Title"
                authors = ', '.join(article.authors) or "Unknown Author"
                source = article.source_url or "Unknown Source"
                text_snippet = article.text[:500].replace("\n", " ") + "..."

                results_html += f"""
                    <li>
                        <strong>Title:</strong> <a href="{link}" target="_blank">{title}</a><br>
                        <strong>Author(s):</strong> {authors}<br>
                        <strong>Source:</strong> {source}<br>
                        <strong>Excerpt:</strong> {text_snippet}
                    </li><hr>
                """
                debug_log.append(f"✅ Successfully extracted article: {title}")
            except Exception as e:
                debug_log.append(f"❌ Failed to extract article: {link}")
                debug_log.append(f"   Error: {str(e)}")
                results_html += f"""
                    <li>
                        <strong>Link:</strong> <a href="{link}" target="_blank">{link}</a><br>
                        <strong>Status:</strong> Failed to extract article.
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