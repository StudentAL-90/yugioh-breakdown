from django.shortcuts import render

from .forms import DeckUploadForm

from services.deck_parser import (
    parse_deck,
    parse_deck_text
)

from services.price_calc import (
    calculate_deck_price
)

from services.deck_storage import (
    save_submitted_cards
)

from services.card_analysis import (
    analyze_deck_cards
)


def upload_deck(request):

    result = None
    card_analysis = None
    analysis_errors = []

    if request.method == "POST":

        form = DeckUploadForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            deck_file = form.cleaned_data.get("deck_file")
            deck_text = form.cleaned_data.get("deck_text", "")
            deck_name = request.POST.get("deck_name", "")

            if deck_text.strip():
                cards = parse_deck_text(deck_text)
                card_source = "manual"
            else:
                cards = parse_deck(deck_file)
                card_source = "file"

            save_submitted_cards(
                cards,
                deck_name=deck_name,
                source=card_source,
            )

            total, breakdown, missing_cards = (
                calculate_deck_price(cards)
            )

            if form.cleaned_data.get("include_card_breakdown"):
                try:
                    card_analysis, analysis_errors = (
                        analyze_deck_cards(cards)
                    )
                except Exception as error:
                    card_analysis = []
                    analysis_errors = [
                        f"AI card breakdown failed: {error}"
                    ]

            result = {
                "total": total,
                "breakdown": breakdown,
                "missing_cards": missing_cards,
            }

    else:

        form = DeckUploadForm()

    return render(
        request,
        "site.html",
        {
            "form": form,
            "result": result,
            "card_analysis": card_analysis,
            "analysis_errors": analysis_errors,
        }
    )
