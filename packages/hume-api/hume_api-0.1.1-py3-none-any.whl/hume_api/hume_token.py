import requests

def fetch_hume_access_token():
    url = "https://app.hume.ai/api/auth/public"
    resp = requests.get(url, timeout=5)
    resp.raise_for_status()
    return resp.json()["token"]
