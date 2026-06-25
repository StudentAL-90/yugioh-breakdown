import requests
from requests import RequestException


BASE_URL = (
    "https://db.ygoprodeck.com/api/v7/cardinfo.php"
)

SESSION = requests.Session()
SESSION.trust_env = False


def get_card_data(card_name):

    try:

        response = SESSION.get(
            BASE_URL,
            params={
                "name": card_name
            },
            timeout=10,
        )

    except RequestException:

        return None

    if response.status_code != 200:
        return None

    data = response.json()

    if "data" not in data:
        return None

    return data["data"][0]
