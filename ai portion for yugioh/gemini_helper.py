import json
import os
import re
from functools import lru_cache

import httpx
import requests
from google import genai
from google.genai import types


MODEL_NAME = "gemini-2.5-flash"


def _get_api_key():
    key_file = os.path.join(
        os.path.dirname(__file__),
        "thestuff.txt",
    )

    if os.path.exists(key_file):
        with open(key_file, "r", encoding="utf-8") as file:
            api_key = file.read().strip()

        if api_key:
            return api_key

    api_key = os.getenv("GEMINI_API_KEY", "").strip()

    if api_key:
        return api_key

    return ""


API_KEY = _get_api_key()

if not API_KEY:
    raise RuntimeError(
        "Set GEMINI_API_KEY before using the Gemini helper."
    )

client = genai.Client(
    api_key=API_KEY,
    http_options=types.HttpOptions(
        httpxClient=httpx.Client(trust_env=False),
        httpxAsyncClient=httpx.AsyncClient(trust_env=False),
    ),
)

BASE_URL = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
SESSION = requests.Session()
SESSION.trust_env = False


def _parse_json_response(text):
    text = text.strip()
    text = text.replace("```json", "")
    text = text.replace("```", "")
    text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.DOTALL)

        if not match:
            raise

        return json.loads(match.group(0))


def get_card_data(name):

    response = SESSION.get(

        BASE_URL,

        params={"name": name}

    )

    data = response.json()

    if "data" in data:

        return data["data"][0]

    return None


@lru_cache(maxsize=5000)

def explain_card(name):

    card = get_card_data(name)

    if card is None:

        return {

            "error":

            f"Could not find {name}"

        }

    prompt = f"""

You are a Yu-Gi-Oh expert.

Explain this card in simple English.

Return ONLY JSON.

{{
"summary":"",
"activates":"",
"stops":[],
"common_uses":[],
"strengths":[],
"weaknesses":[]
}}

Card Name:

{card["name"]}

Card Type:

{card["type"]}

Description:

{card["desc"]}

"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )

    return _parse_json_response(response.text)


def explain_cards(names):

    cards = []

    for name in names:

        card = get_card_data(name)

        if card:

            cards.append(card)

    if len(cards) == 0:

        return {

            "error":

            "No cards found"

        }

    card_text = ""

    for card in cards:

        card_text += f"""

Name:

{card["name"]}

Type:

{card["type"]}

Description:

{card["desc"]}

----------------------

"""

    prompt = f"""

You are a Yu-Gi-Oh expert.

Explain how these cards work together.

Return ONLY JSON.

{{

"deck_strategy":"",

"synergies":[],

"opening_plays":[],

"strengths":[],

"weaknesses":[]

}}

Cards:

{card_text}

"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )

    return _parse_json_response(response.text)
