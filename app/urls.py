from django.urls import path

from services.views import upload_deck

urlpatterns = [

    path(
        "",
        upload_deck,
        name="upload_deck"
    ),
]