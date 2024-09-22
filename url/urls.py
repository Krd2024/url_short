from venv import create
from django.urls import path
from .views import index, shorten_url  # Замените на ваше представление

urlpatterns = [
    path("", index, name="index"),  # Или любой другой путь, который вы хотите
    path("url_short/", shorten_url, name="new_url_db"),
]
