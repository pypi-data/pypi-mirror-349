import requests
from typing import Dict, Any, List

def get_masked_data(base_url: str, token: str, table_name: str, is_masked: bool = True, filters: Dict[str, Any] = {}) -> List[Dict[str, Any]]:
    url = f"{base_url}/api/masking/query/"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "table_name": table_name,
        "is_masked": is_masked,
        "filters": filters
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()
