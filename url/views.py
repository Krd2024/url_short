from urllib.parse import urlparse
from django.shortcuts import render
from hashids import Hashids

from url.models import Handler


# shortener/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt  # Используйте только для тестирования. В реальном приложении используйте CSRF-токены.
def shorten_url(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            url = data.get("url")
            short_url = data.get("shortUrl")
            print(url, short_url)

            # Здесь вы можете добавить логику для обработки URL, например, сохранение в базе данных

            return JsonResponse(
                {
                    "message": "Сокращенный URL создан!",
                    "url": url,
                    "shortUrl": short_url,
                }
            )
        except json.JSONDecodeError:
            print("error: Неверный формат данных")
            return JsonResponse({"error": "Неверный формат данных"}, status=400)

    return JsonResponse({"error": "Метод не разрешен."}, status=405)


def create(request):

    x = "http://aaaaa.ru/111111"

    new_url_db = Handler(url=x)
    new_url_db.save()
    print(new_url_db, "< ----result new url")
    parsed_url = urlparse(x)
    domain = parsed_url.netloc
    print(domain, "< ---- domain is created")

    # path = parsed_url.path

    hashids = Hashids(min_length=8, salt="your_salt_here")

    # Кодирование
    # original_string = url
    # hashed_id = hashids.encode_hex(original_string.encode().hex())
    # print(f"Hashed: {hashed_id}")

    # Декодирование
    # decoded = bytes.fromhex(hashids.decode_hex(hashed_id)).decode()
    # print(f"Decoded: {decoded}")


def index(request, url=None):
    print(url)
    create(url)
    return render(request, "index.html", {"test": True})


# Create your views here.
