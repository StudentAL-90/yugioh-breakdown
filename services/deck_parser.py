def parse_deck(uploaded_file):

    content = uploaded_file.read().decode("utf-8")

    return parse_deck_text(content)


def parse_deck_text(deck_text):

    cards_by_name = {}

    for line in deck_text.splitlines():

        line = line.strip()

        if not line or line.startswith("#"):
            continue

        parts = line.split(" ", 1)

        if len(parts) == 2 and parts[0].isdigit():
            qty = int(parts[0])
            card_name = parts[1].strip()
        else:
            qty = 1
            card_name = line

        if qty <= 0 or not card_name:
            continue

        cards_by_name[card_name] = (
            cards_by_name.get(card_name, 0) + qty
        )

    return [
        {
            "quantity": quantity,
            "name": name,
        }
        for name, quantity in cards_by_name.items()
    ]
