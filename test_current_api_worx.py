"""
{
    "details": "{\"status\":\"429\",\"msg\":\"API quota exceeded. Upgrade plan or wait for reset.\"}",
    "error": "⚠️ Failed to fetch data from Currents API"


    Ahhh there it is — this line says it all:

    json
    Kopírovať
    Upraviť
    "msg":"API quota exceeded. Upgrade plan or wait for reset."
    You’ve hit your Currents API free plan limit (status code 429 = Too Many Requests). 😅 Nothing’s wrong with your code anymore — the API is just blocking you until:

    Your quota resets (usually daily or monthly — check CurrentsAPI dashboard for details), or

    You upgrade your plan to get more requests.

    Options now:
    Option 1: Wait for quota reset
    If you’re just testing, this might be fine. Come back later and it should start working again.

    Option 2: Create a new API key
    If this is just a sandbox account and you're okay with starting fresh, you can:

    Create a new Currents API account.

    Use the new key.

    Update your Render environment variable with the new CURRENTS_API_KEY.

    Option 3: Upgrade your Currents API plan
    If you’re going into production or want higher limits, upgrading is the most stable way.

    If you want to test code functionality without hitting CurrentsAPI again, I can help you mock the API response using test data so you can still build the front end or check how your JSON output looks.

    Want to go that route while waiting?







    Tvoje slová:
    i see. lets put it on hold. i ll remain this to a different name and you write me a new app.py to access the google and we will finish the selenium hack to get around the javascript obstacle we finished at before. do you remember the working google connection or do you want me to give it back to you?

}
"""



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
    API_ENDPOINT = "https://api.currentsapi.services/v1/search"
    params = {
        "keywords": SEARCH_QUERY,
        "language": "en"
    }

    headers = {
        "Authorization": CURRENTS_API_KEY
    }

    print("🌐 Connecting to Currents API...")
    print("📍 Endpoint:", API_ENDPOINT)
    print("🔐 Headers:", headers)
    print("🧾 Params:", params)

    try:
        response = requests.get(API_ENDPOINT, headers=headers, params=params)
        print(f"📡 Response Status Code: {response.status_code}")
        print("🔍 Raw response text (truncated):", response.text[:300])

        if response.status_code != 200:
            print("⚠️ Non-200 status code received.")
            return jsonify({"error": "⚠️ Failed to fetch data from Currents API", "details": response.text}), response.status_code

        try:
            data = response.json()
            print("📦 Successfully parsed JSON.")
        except Exception as json_err:
            print("❌ Failed to parse JSON:", json_err)
            return jsonify({"error": "❌ Failed to parse JSON", "details": response.text}), 500

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