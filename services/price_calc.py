from decimal import Decimal

from services.YGO_PROapi import get_card_data


def calculate_deck_price(cards):

    total = Decimal("0.00")

    breakdown = []
    missing_cards = []

    for card in cards:

        card_data = get_card_data(
            card["name"]
        )

        if not card_data:
            missing_cards.append(card["name"])
            continue

        try:

            price = Decimal(
                card_data["card_prices"][0]
                ["tcgplayer_price"]
            )

        except (KeyError, IndexError, TypeError):

            price = Decimal("0")

        subtotal = (
            price *
            card["quantity"]
        )

        total += subtotal

        breakdown.append({
            "name": card["name"],
            "quantity": card["quantity"],
            "price_each": price,
            "subtotal": subtotal
        })

    return total, breakdown, missing_cards
