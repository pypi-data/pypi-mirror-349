import requests
from typing import List

def fetch_rules(base_url: str, table_id: int, token: str) -> List[dict]:
    url = f"{base_url}/api/rules/table/{table_id}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()
