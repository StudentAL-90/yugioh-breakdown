import sqlite3


# ==========================
# Connect to Database
# ==========================

conn = sqlite3.connect("yugioh_deck.db")

cursor = conn.cursor()


# ==========================
# Create Tables
# ==========================

cursor.execute("""

CREATE TABLE IF NOT EXISTS decks(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    deck_name TEXT NOT NULL UNIQUE

)

""")


cursor.execute("""

CREATE TABLE IF NOT EXISTS deck_cards(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    deck_id INTEGER,

    card_name TEXT NOT NULL,

    amount INTEGER NOT NULL CHECK(

        amount >= 1

        AND

        amount <= 3

    ),

    UNIQUE(deck_id, card_name),

    FOREIGN KEY(deck_id)

    REFERENCES decks(id)

)

""")

conn.commit()


# ==========================
# Functions
# ==========================

def create_deck(deck_name):

    cursor.execute("""

    INSERT OR IGNORE INTO decks(

        deck_name

    )

    VALUES(?)

    """,(deck_name,))

    conn.commit()

    print(f"Deck '{deck_name}' created.")



def add_card(deck_name, card_name, amount):

    cursor.execute("""

    SELECT id

    FROM decks

    WHERE deck_name = ?

    """,(deck_name,))

    deck = cursor.fetchone()

    if deck is None:

        print("Deck not found.")

        return

    deck_id = deck[0]


    cursor.execute("""

    INSERT INTO deck_cards(

        deck_id,

        card_name,

        amount

    )

    VALUES(

        ?, ?, ?

    )

    ON CONFLICT(

        deck_id,

        card_name

    )

    DO UPDATE SET

    amount = excluded.amount

    """,(

        deck_id,

        card_name,

        amount

    ))

    conn.commit()

    print(f"{amount}x {card_name} added to {deck_name}")



def remove_card(deck_name, card_name):

    cursor.execute("""

    SELECT id

    FROM decks

    WHERE deck_name = ?

    """,(deck_name,))

    deck = cursor.fetchone()

    if deck is None:

        print("Deck not found.")

        return

    deck_id = deck[0]


    cursor.execute("""

    DELETE FROM deck_cards

    WHERE

    deck_id = ?

    AND

    card_name = ?

    """,(

        deck_id,

        card_name

    ))

    conn.commit()

    print(f"{card_name} removed.")



def view_deck(deck_name):

    cursor.execute("""

    SELECT id

    FROM decks

    WHERE deck_name = ?

    """,(deck_name,))

    deck = cursor.fetchone()

    if deck is None:

        print("Deck not found.")

        return

    deck_id = deck[0]


    cursor.execute("""

    SELECT

        card_name,

        amount

    FROM deck_cards

    WHERE deck_id = ?

    ORDER BY card_name

    """,(deck_id,))

    cards = cursor.fetchall()


    print()

    print("=" * 30)

    print(deck_name)

    print("=" * 30)

    print()


    if not cards:

        print("Deck empty.")

        return


    for card_name, amount in cards:

        print(

            f"{amount}x {card_name}"

        )


    print()

    print(

        "Total Cards:",

        total_cards(deck_name)

    )



def total_cards(deck_name):

    cursor.execute("""

    SELECT id

    FROM decks

    WHERE deck_name = ?

    """,(deck_name,))

    deck = cursor.fetchone()

    if deck is None:

        return 0

    deck_id = deck[0]


    cursor.execute("""

    SELECT SUM(amount)

    FROM deck_cards

    WHERE deck_id = ?

    """,(deck_id,))

    total = cursor.fetchone()[0]

    return total if total else 0



def list_decks():

    cursor.execute("""

    SELECT deck_name

    FROM decks

    ORDER BY deck_name

    """)

    decks = cursor.fetchall()

    print()

    print("YOUR DECKS")

    print("-" * 20)

    print()

    if not decks:

        print("No decks.")

        return

    for deck in decks:

        print(deck[0])



# ==========================
# Menu Loop
# ==========================

while True:

    print()

    print("1 - Create Deck")

    print("2 - Add Card")

    print("3 - Remove Card")

    print("4 - View Deck")

    print("5 - List Decks")

    print("6 - Exit")

    print()


    choice = input("Choice: ")


    if choice == "1":

        deck_name = input(

            "Deck Name: "

        )

        create_deck(deck_name)



    elif choice == "2":

        deck_name = input(

            "Deck Name: "

        )

        card_name = input(

            "Card Name: "

        )

        amount = int(

            input(

                "Amount (1-3): "

            )

        )

        add_card(

            deck_name,

            card_name,

            amount

        )



    elif choice == "3":

        deck_name = input(

            "Deck Name: "

        )

        card_name = input(

            "Card Name: "

        )

        remove_card(

            deck_name,

            card_name

        )



    elif choice == "4":

        deck_name = input(

            "Deck Name: "

        )

        view_deck(

            deck_name

        )



    elif choice == "5":

        list_decks()



    elif choice == "6":

        break



    else:

        print("Invalid choice.")



# ==========================
# Close Database
# ==========================

conn.close()