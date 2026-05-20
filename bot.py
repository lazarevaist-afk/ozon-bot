import requests

def search_ozon(query):
    url = "https://www.ozon.ru/api/entrypoint-api.bx/page/json/v2"

    params = {
        "url": f"/search/?text={query}"
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    r = requests.get(url, params=params, headers=headers, timeout=10)
    data = r.json()

    results = []

    try:
        blocks = data.get("widgetStates", {})

        for key, value in blocks.items():
            if "searchResultsV2" in key:
                import json
                parsed = json.loads(value)

                items = parsed.get("items", [])

                for item in items:
                    title = item.get("title")
                    product_id = item.get("action", {}).get("id")

                    link = f"https://www.ozon.ru/product/{product_id}"

                    seller = item.get("seller", {}).get("name", "не указан")

                    results.append({
                        "title": title,
                        "link": link,
                        "seller": seller
                    })

    except Exception:
        pass

    return results
