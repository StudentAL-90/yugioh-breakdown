def classify_card(card):
    name = card["name"].lower()
    desc = card.get("desc", "").lower()
    categories = []

    # -------------------------
    # Hand Trap
    # -------------------------
    handtrap_patterns = [
        "from your hand",
        "during your opponent",
        "when your opponent",
        "if your opponent",
        "quick effect",
        "negate the activation",
        "negate its effects",
        "discard this card",
        "send this card from your hand"
    ]

    ghost_girls = {
        "ash blossom & joyous spring",
        "ghost ogre & snow rabbit",
        "ghost belle & haunted mansion",
        "ghost reaper & winter cherries",
        "ghost sister & spooky dogwood",
        "ghost mourner & moonlit chill"
    }

    mulcharmys = {
        "mulcharmy fuwalos",
        "mulcharmy purulia",
        "mulcharmy meowls"
    }

    is_handtrap = False

    if any(x in desc for x in handtrap_patterns):
        if (
            "from your hand" in desc or
            "discard this card" in desc or
            "send this card from your hand" in desc
        ):
            is_handtrap = True

    if name in ghost_girls:
        is_handtrap = True

    if name in mulcharmys:
        is_handtrap = True

    if is_handtrap:
        categories.append("Hand Trap")

    # -------------------------
    # Starter
    # -------------------------
    starter_patterns = [
        "add 1",
        "add",
        "search",
        "from your deck to your hand",
        "send 1",
        "from your deck to the graveyard",
        "special summon 1",
        "from your deck",
        "if this card is normal summoned",
        "if this card is summoned",
        "when this card is summoned"
    ]

    if any(x in desc for x in starter_patterns):
        categories.append("Starter")

    # -------------------------
    # Extender
    # -------------------------
    extender_patterns = [
        "special summon this card",
        "special summon it",
        "from your hand",
        "from your graveyard",
        "if you control",
        "if you have",
        "banish this card",
        "discard this card",
        "target 1 monster in your graveyard",
        "special summon 1 monster"
    ]

    if any(x in desc for x in extender_patterns):
        categories.append("Extender")

    # -------------------------
    # Payoff
    # -------------------------
    payoff_patterns = [
        "cannot be targeted",
        "cannot be destroyed",
        "your opponent cannot",
        "unaffected by",
        "negate",
        "destroy all",
        "banish all",
        "inflict",
        "double battle damage",
        "once per turn",
        "gains",
        "atk becomes"
    ]

    if any(x in desc for x in payoff_patterns):
        categories.append("Payoff")

    # -------------------------
    # Worth-it / "Does Nothing" analysis
    # -------------------------
    if len(categories) == 0:
        worth_label = evaluate_low_value_card(desc)
        categories.append(worth_label)

    return categories


def evaluate_low_value_card(desc):
    """
    Heuristic scoring for cards with no obvious role keywords.
    Returns a more useful label than 'Does Nothing'.
    """

    setup_cost = 0
    payoff = 0
    restriction = 0

    # Cost / difficulty markers
    cost_patterns = {
        "discard": 1,
        "send 1": 1,
        "send this card": 1,
        "banish this card": 1,
        "tribute": 2,
        "tribute 1": 2,
        "tribute 2": 3,
        "except": 2,
        "if you control": 1,
        "if you have": 1,
        "during the end phase": 1,
        "during your next turn": 2,
        "once per duel": 4,
        "skip your battle phase": 3,
        "cannot attack": 2,
        "cannot special summon": 4,
        "lock": 2
    }

    payoff_patterns = {
        "draw 1": 1,
        "add 1 card": 2,
        "special summon": 3,
        "destroy": 2,
        "banish": 3,
        "negate": 4,
        "send to the graveyard": 2,
        "search": 3,
        "double": 2,
        "recover": 1,
        "gain": 1,
        "inflict": 2,
        "cannot be targeted": 3,
        "cannot be destroyed": 3,
        "unaffected by": 5
    }

    restriction_patterns = {
        "for the rest of this turn": 1,
        "for the rest of this duel": 4,
        "during your opponent's turn": 1,
        "only once per turn": 1,
        "once per turn": 1,
        "only if": 1,
        "you can only": 2,
        "except": 2,
        "cannot": 2
    }

    # Score cost
    for pattern, score in cost_patterns.items():
        if pattern in desc:
            setup_cost += score

    # Score payoff
    for pattern, score in payoff_patterns.items():
        if pattern in desc:
            payoff += score

    # Score restrictions
    for pattern, score in restriction_patterns.items():
        if pattern in desc:
            restriction += score

    total_difficulty = setup_cost + restriction

    # Decide label
    if payoff == 0 and total_difficulty >= 3:
        return "Does Nothing"

    if payoff <= 2 and total_difficulty >= 4:
        return "Too Hard for the Reward"

    if payoff <= 2 and total_difficulty >= 2:
        return "Niche / Situational"

    if payoff >= 4 and total_difficulty >= 5:
        return "Strong but Hard to Use"

    if payoff >= 3 and total_difficulty <= 2:
        return "Worth It"

    return "Low Impact"