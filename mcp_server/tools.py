# mcp_server/tools.py

def search_web(query: str):
    return {"query": query, "results": []}

def fetch_url(url: str):
    return {"url": url, "content": ""}

def clean_extract(raw_text: str):
    return raw_text.strip()

def extract_entities(text: str):
    return {
        "competitors": [],
        "pricing": [],
        "themes": []
    }

def dedupe_items(items: list):
    return list(set(items))

def impact_score(item: dict, context: dict):
    return {
        "impact_level": "Medium",
        "score": 50,
        "why": ["Initial placeholder"],
        "actions": ["Review manually"]
    }

def generate_market_report(data: dict):
    return data
