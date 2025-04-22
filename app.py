from flask import Flask
import requests

app = Flask(__name__)

@app.route("/test")
def test_api():
    url = "https://api.db.nomics.world/v22/series/NBS/A_A060F01/A060F010B"
    try:
        response = requests.get(url, timeout=5)
        return f"✅ Status: {response.status_code}<br><br>{response.text[:500]}"
    except Exception as e:
        return f"❌ Error: {e}"

@app.route("/")
def home():
    return "Welcome to the API test app! Visit <code>/test</code> to run the test."
