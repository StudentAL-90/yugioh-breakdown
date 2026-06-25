from django import forms


class DeckUploadForm(forms.Form):

    deck_text = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 10,
                "placeholder": (
                    "Example:\n"
                    "3 Blue-Eyes White Dragon\n"
                    "2 Ash Blossom & Joyous Spring\n"
                    "Dark Magician"
                ),
            }
        ),
        label="Paste Deck List",
    )

    deck_file = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                "class": "form-control",
            }
        ),
        label="Or Upload Deck List",
    )

    include_card_breakdown = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input",
            }
        ),
        label="Show AI card breakdown",
    )

    def clean(self):
        cleaned_data = super().clean()

        deck_text = cleaned_data.get("deck_text", "").strip()
        deck_file = cleaned_data.get("deck_file")

        if not deck_text and not deck_file:
            raise forms.ValidationError(
                "Paste a deck list or upload a deck list file."
            )

        return cleaned_data
