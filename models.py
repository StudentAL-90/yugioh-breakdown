from django.db import models


class DeckSubmission(models.Model):

    uploaded_file = models.FileField(
        upload_to="decks/"
    )

    deck_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Deck #{self.id}"