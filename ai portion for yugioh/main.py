from gemini_helper import explain_card
from gemini_helper import explain_cards


# Single card

result = explain_card(

    "Ash Blossom & Joyous Spring"

)

print()

print("SUMMARY")

print(result["summary"])

print()

print("ACTIVATES")

print(result["activates"])

print()

print("COMMON USES")

for item in result["common_uses"]:

    print("-", item)

print()

print("STRENGTHS")

for item in result["strengths"]:

    print("-", item)

print()

print("WEAKNESSES")

for item in result["weaknesses"]:

    print("-", item)



print("\n====================\n")


# Multiple cards

combo = explain_cards([

    "Snake-Eye Ash",

    "Diabellstar the Black Witch",

    "Original Sinful Spoils - Snake-Eye"

])


print("DECK STRATEGY")

print(combo["deck_strategy"])

print()

print("SYNERGIES")

for item in combo["synergies"]:

    print("-", item)

print()

print("OPENING PLAYS")

for item in combo["opening_plays"]:

    print("-", item)