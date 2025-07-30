import requests

def osintcat(cat_id="", module="", query=""):
    base_url = f"https://osintcat.ru/api/{module}?query={query}&id={cat_id}"
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}
def parse(data):
    if not isinstance(data, dict):
        return str(data)

    result = []
    for key, value in data.items():
        if isinstance(value, list):
            value_str = ", ".join(str(item) for item in value)
        elif isinstance(value, dict):
            sub = parse(value)
            value_str = f"{{{sub}}}"
        else:
            value_str = str(value)
        result.append(f"{key}: {value_str}")
    return "\n".join(result)