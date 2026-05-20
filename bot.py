import requests
import json

def search_ozon(query):
    url = "https://www.ozon.ru/api/entrypoint-api.bx/page/json/v2"

    params = {
        "url": f"/search/?text={query}"
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    try:
        r = requests.get(url, params=params, headers=headers, timeout=10)
        r.raise_for_status()
        data = r.json()

        results = []

        blocks = data.get("widgetStates", {})

        for key, value in blocks.items():
            if "searchResultsV2" in key:
                parsed = json.loads(value)

                items = parsed.get("items", [])

                for item in items:
                    title = item.get("title", "без названия")

                    product_id = None
                    action = item.get("action")

                    if isinstance(action, dict):
                        product_id = action.get("id")

                    if product_id:
                        link = f"https://www.ozon.ru/product/{product_id}"
                    else:
                        link = "нет ссылки"

                    seller = "не указан"
                    if isinstance(item.get("seller"), dict):
                        seller = item["seller"].get("name", "не указан")

                    results.append({
                        "title": title,
                        "link": link,
                        "seller": seller
                    })

        return results

    except Exception as e:
        print("❌ ERROR IN OZON SEARCH:", e)
        return []
