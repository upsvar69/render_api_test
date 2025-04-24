from flask import Flask
import requests

app = Flask(__name__)

URLS = {
    "DBnomics": "https://api.db.nomics.world/v22/series/NBS/A_A060F01/A060F010B",
    "BBC": "https://www.bbc.com",
    "Reuters": "https://www.reuters.com",
    "Al Jazeera": "https://www.aljazeera.com",
    "NPR": "https://www.npr.org",
}


@app.route("/test")

def test_api():
    results = []
    for name, url in URLS.items():
        try:
            response = requests.get(url, timeout=5)
            results.append(f"✅ <strong>{name}</strong>: Status {response.status_code}")
        except Exception as e:
            results.append(f"❌ <strong>{name}</strong>: Error - {e}")
    return "<br><br>".join(results)
"""
def test_api():
    url = "https://api.db.nomics.world/v22/series/NBS/A_A060F01/A060F010B"
    try:
        response = requests.get(url, timeout=5)
        return f"✅ Status: {response.status_code}<br><br>{response.text[:500]}"
    except Exception as e:
        return f"❌ Error: {e}"
"""


@app.route("/")
def home():
    return (
        "Welcome to the API test app!<br>"
        "Visit <code>/test</code> to run connectivity checks for:<br>"
        "<ul>"
        "<li>DBnomics</li>"
        "<li>BBC</li>"
        "<li>Reuters</li>"
        "<li>Al Jazeera</li>"
        "<li>NPR</li>"
        "</ul>"
    )
