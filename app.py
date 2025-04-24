import requests
from flask import Flask, jsonify
import os

app = Flask(__name__)

CURRENTS_API_KEY = os.getenv("CURRENTS_API_KEY")
if not CURRENTS_API_KEY:
    return jsonify({"error": "❌ CURRENTS_API_KEY not set"}), 500
SEARCH_QUERY = "belt and road"
API_ENDPOINT = f"https://api.currentsapi.services/v1/search?keywords={SEARCH_QUERY}&language=en"

@app.route("/")
def get_news():
    print("🌐 Connecting to Currents API...")
    try:
        response = requests.get(
            API_ENDPOINT,
            headers={"Authorization": CURRENTS_API_KEY}
        )
        print(f"📡 Currents API response: {response.status_code}")
        data = response.json()
    except Exception as e:
        print("❌ Error fetching data:", e)
        return jsonify({"message": "❌ Failed to fetch news."})

    if "news" not in data or not data["news"]:
        print("❗ No articles found.")
        return jsonify({"message": f"❗ No articles found mentioning '{SEARCH_QUERY}' AGAIN!"})

    print(f"✅ Found {len(data['news'])} articles mentioning '{SEARCH_QUERY}'.")

    articles = [
        {
            "title": article["title"],
            "url": article["url"],
            "source": article["source"],
            "published": article["published"]
        }
        for article in data["news"][:5]
    ]

    return jsonify({
        "message": f"🔍 Top {len(articles)} articles mentioning '{SEARCH_QUERY}':",
        "articles": articles
    })