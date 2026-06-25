from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

from services.YGO_PROapi import get_card_data


BASE_DIR = Path(__file__).resolve().parent.parent
CARD_CHECKER_PATH = BASE_DIR / "ai portion for yugioh" / "card checker.py"
GEMINI_HELPER_PATH = BASE_DIR / "ai portion for yugioh" / "gemini_helper.py"


def _load_card_checker():
    spec = spec_from_file_location(
        "ygo_card_checker",
        CARD_CHECKER_PATH,
    )

    if spec is None or spec.loader is None:
        return None

    module = module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def _load_gemini_helper():
    spec = spec_from_file_location(
        "ygo_gemini_helper",
        GEMINI_HELPER_PATH,
    )

    if spec is None or spec.loader is None:
        return None

    module = module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def analyze_deck_cards(cards):
    card_checker = _load_card_checker()

    if card_checker is None:
        return [], [
            "Could not load the card checker from the AI folder."
        ]

    gemini_helper = None
    try:
        gemini_helper = _load_gemini_helper()
    except RuntimeError as error:
        gemini_helper = None
        gemini_error = str(error)
    except Exception as error:
        gemini_helper = None
        gemini_error = f"Could not load Gemini helper: {error}"
    else:
        gemini_error = ""

    analysis = []
    errors = []

    if gemini_error:
        errors.append(gemini_error)

    for card in cards:
        card_data = get_card_data(card["name"])

        if not card_data:
            errors.append(f"Could not find {card['name']}")
            continue

        categories = card_checker.classify_card(card_data)
        ai_explanation = None

        if gemini_helper:
            try:
                explanation = gemini_helper.explain_card(card_data["name"])
            except Exception as error:
                errors.append(
                    f"Gemini could not explain {card_data['name']}: {error}"
                )
            else:
                if "error" in explanation:
                    errors.append(explanation["error"])
                else:
                    ai_explanation = explanation

        analysis.append(
            {
                "name": card_data["name"],
                "quantity": card["quantity"],
                "type": card_data.get("type", "Unknown"),
                "race": card_data.get("race", ""),
                "attribute": card_data.get("attribute", ""),
                "level": card_data.get("level"),
                "atk": card_data.get("atk"),
                "def": card_data.get("def"),
                "description": card_data.get("desc", ""),
                "categories": categories,
                "ai_explanation": ai_explanation,
            }
        )

    return analysis, errors
