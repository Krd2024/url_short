from django.urls import path
from .views import index, shorten_url, url_delete, url_short_get

urlpatterns = [
    path("", index, name="index"),
    path("url_short/", shorten_url, name="new_url_db"),
    path("url_short_get/", url_short_get, name="url_short_get"),
    path("api/urls/<int:id>/", url_delete, name="url_delete"),
]
