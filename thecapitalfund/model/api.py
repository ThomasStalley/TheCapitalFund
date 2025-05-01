import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("API_KEY")


def api_get_request(data_slug: str, data_key: str):
    """Perform GET request to capital API, to grab day, member or transaction data."""
    url = f"https://capitool.auchester.com/{data_slug}/"
    headers = {"API-KEY": api_key}
    request = requests.get(url=url, headers=headers)
    # check if the request was successful:
    if request.status_code != 200:
        print(f"Request for {data_key.lower()} data failed with status code: {request.status_code}")
        return None
    try:
        response = json.loads(request.text)
        chosen_data = response.get(data_key)
        return chosen_data
    except json.JSONDecodeError:
        print("Failed to parse JSON from response:", request.text)
        return None
