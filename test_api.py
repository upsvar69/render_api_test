import requests

def test_api():
    url = "https://api.db.nomics.world/v22/series/NBS/A_A060F01/A060F010B"  # replace with the real one
    try:
        response = requests.get(url, timeout=5)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:200]}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_api()
