import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "yugioh_deck.db"


def _connect():
    return sqlite3.connect(DATABASE_PATH)


def ensure_submitted_cards_table():
    with _connect() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS submitted_cards(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                deck_name TEXT NOT NULL,
                source TEXT NOT NULL,
                card_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def save_submitted_cards(cards, deck_name="", source="manual"):
    ensure_submitted_cards_table()

    clean_deck_name = deck_name.strip() or "Untitled Deck"

    rows = [
        (
            clean_deck_name,
            source,
            card["name"],
            card["quantity"],
        )
        for card in cards
    ]

    if not rows:
        return

    with _connect() as connection:
        connection.executemany(
            """
            INSERT INTO submitted_cards(
                deck_name,
                source,
                card_name,
                quantity
            )
            VALUES(?, ?, ?, ?)
            """,
            rows,
        )
