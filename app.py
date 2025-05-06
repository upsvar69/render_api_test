from flask import Flask
from duckduckgo_search import DDGS
from newspaper import Article
import traceback

app = Flask(__name__)

SEARCH_QUERY = "Belt and Road Initiative"

@app.route("/")
def home():
    debug_log = []
    results_html = "<h1>🔗 Articles on Belt and Road Initiative (via DuckDuckGo)</h1><ul>"
    article_count = 0

    try:
        debug_log.append("🔍 Starting DuckDuckGo search...")
        with DDGS() as ddgs:
            search_results = ddgs.text(SEARCH_QUERY, max_results=10)
            for result in search_results:
                if article_count >= 10:
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

        results_html += "</ul>"

    except Exception as e:
        debug_log.append(f"❌ Critical error: {str(e)}")
        debug_log.append(traceback.format_exc())
        results_html = "<h1>❌ Error during processing</h1>"

    debug_html = "<hr><h2>🧪 Debug Info</h2><pre>" + "\n".join(debug_log) + "</pre>"
    return results_html + debug_html