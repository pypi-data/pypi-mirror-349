import requests

def osintcat(cat_id="", module="", query=""):
    base_url = f"https://osintcat.ru/api/{module}?query={query}&id={cat_id}"
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}
