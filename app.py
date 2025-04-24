import requests
from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route("/")
def get_news():
    print("🚀 Starting request...")

    CURRENTS_API_KEY = os.getenv("CURRENTS_API_KEY")
    if not CURRENTS_API_KEY:
        print("❌ API key not found in environment variables!")
        return jsonify({"error": "❌ CURRENTS_API_KEY not set"}), 500

    print("🔑 API key loaded successfully.")

    SEARCH_QUERY = "belt and road"
    API_ENDPOINT = f"https://api.currentsapi.services/v1/search"
    params = {
        "keywords": SEARCH_QUERY,
        "language": "en"
    }

    headers = {
        "Authorization": CURRENTS_API_KEY
    }

    print("🌐 Connecting to Currents API...")
    try:
        response = requests.get(API_ENDPOINT, headers=headers, params=params)
        print(f"📡 Currents API response status: {response.status_code}")

        if response.status_code != 200:
            print("⚠️ Non-200 response received!")
            print("🔍 Response text:", response.text)
            return jsonify({"error": "⚠️ Failed to fetch data from Currents API"}), response.status_code

        data = response.json()
        print("📦 JSON response received.")

    except Exception as e:
        print("❌ Exception occurred during request:", e)
        return jsonify({"error": "❌ Failed to fetch news due to exception."}), 500

    if "news" not in data or not data["news"]:
        print("❗ No articles found in API response.")
        return jsonify({"message": f"❗ No articles found mentioning '{SEARCH_QUERY}'."}), 200

    print(f"✅ Found {len(data['news'])} articles mentioning '{SEARCH_QUERY}'.")

    articles = [
        {
            "title": article.get("title"),
            "url": article.get("url"),
            "source": article.get("source"),
            "published": article.get("published")
        }
        for article in data["news"][:5]
    ]

    return jsonify({
        "message": f"🔍 Top {len(articles)} articles mentioning '{SEARCH_QUERY}':",
        "articles": articles
    }), 200

if __name__ == "__main__":
    app.run(debug=True)