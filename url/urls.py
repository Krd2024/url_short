from venv import create
from django.urls import path

from url.parser import my_view
from .views import index, shorten_url, url_short_get  # Замените на ваше представление

urlpatterns = [
    path("", index, name="index"),  # Или любой другой путь, который вы хотите
    path("url_short/", shorten_url, name="new_url_db"),
    path("my_view/", my_view, name="new_umy_viewrl_db"),
    path("url_short_get/", url_short_get, name="url_short_get"),
]
