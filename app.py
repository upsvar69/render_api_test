from flask import Flask, jsonify
import feedparser

app = Flask(__name__)

BBC_FEEDS = {
    "World": "http://feeds.bbci.co.uk/news/world/rss.xml",
    "Asia": "http://feeds.bbci.co.uk/news/world/asia/rss.xml",
    "Top Stories": "http://feeds.bbci.co.uk/news/rss.xml",
}

KEYWORDS = ["belt and road", "belt & road", "一带一路"]

def fetch_articles():
    found_articles = []
    print("🔍 Search Results:")
    for name, url in BBC_FEEDS.items():
        print(f"🌐 Connecting to {name} feed...")
        feed = feedparser.parse(url)
        if not feed.entries:
            print(f"⚠️ No entries found in {name}")
            continue
        print(f"✅ Successfully parsed {len(feed.entries)} entries from {name}")
        for entry in feed.entries:
            title = entry.get("title", "").lower()
            summary = entry.get("summary", "").lower()
            if any(keyword in title or keyword in summary for keyword in KEYWORDS):
                found_articles.append({
                    "title": entry.get("title"),
                    "link": entry.get("link"),
                    "published": entry.get("published", "N/A")
                })
        if len(found_articles) >= 5:
            break
    return found_articles[:5]

@app.route("/")
def index():
    print("🔗 BBC Articles on Belt and Road Initiative (via RSS)")
    articles = fetch_articles()
    if not articles:
        return jsonify({"message": "❗ No articles found mentioning 'Belt and Road'."}), 200
    return jsonify({"articles": articles}), 200

if __name__ == "__main__":
    app.run(debug=True)