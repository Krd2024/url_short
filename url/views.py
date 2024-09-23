from pyexpat.errors import messages
from urllib.parse import urlparse
from django.db import IntegrityError
from django.shortcuts import render
from hashids import Hashids

from url import config
from url.models import Handler

from django.core.validators import URLValidator

from django.core.exceptions import ValidationError

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from url.parser import my_view


def custom_url_validator(value):
    print(value, "< ------ value")
    if not value.startswith("http://") and not value.startswith("https://"):
        print("URL должен начинаться с http:// или https://")
        return False
        #     raise ValidationError("URL должен начинаться с http:// или https://")
        # elif not value.endswith(config.LIST):
        #     return False
        #     raise ValidationError("URL должен заканчиваться по-другому")

    else:
        return True
        print("Всё нормально")


@csrf_exempt  # Используйте только для тестирования. В реальном приложении используйте CSRF-токены.
def shorten_url(request):
    if request.method == "POST":
        my_view(request)
        try:
            data = json.loads(request.body)
            url = data.get("url")

            if not custom_url_validator(url):
                return JsonResponse({"error": "Неверный формат данных"}, status=400)

            new_url_db = Handler(url=url)
            new_url_db.save()

            return JsonResponse(
                {
                    "message": "Сокращенный URL создан!",
                    "url": url,
                    "shortUrl": new_url_db.new_url,
                }
            )
        except IntegrityError:
            print("ДУБЛЬ")
            # Если Url уже существует вернуть уже сформированный короткий Url
            url_obj = Handler.objects.get(url=url)
            return JsonResponse({"new_url": url_obj.new_url}, status=405)

        except json.JSONDecodeError:
            print("error: Неверный формат данных")
            return JsonResponse({"error": "Неверный формат данных"}, status=400)

    return JsonResponse({"error": "Метод не разрешен-2."}, status=405)


@csrf_exempt
def url_short_get(request):
    """Проверить и перейти по короткому Url"""

    if request.method == "POST":
        my_view(request)
        try:
            data = json.loads(request.body)
            short_url = data.get("shortUrl_go")
            # Получить токен адреса
            token_url = short_url.split("/")
            print(token_url[1], "< ---- token")
            try:
                real_url = Handler.objects.get(token=token_url[1])
                print(f"{real_url.url} - полный Url для {short_url}")
                return JsonResponse(
                    {
                        "url": real_url.url,
                    }
                )
            except Handler.DoesNotExist:
                print(f"Нет соответствующей записи")
        except Exception as e:
            print(e)

        except json.JSONDecodeError:
            print("error: Неверный формат данных")
        #     return JsonResponse({"error": "Неверный формат данных"}, status=400)

    return JsonResponse({"error": "Нет соответствующей записи"}, status=405)


# def create(request):

#     x = "http://aaaaa.ru/111111"

#     new_url_db = Handler(url=x)
#     new_url_db.save()
#     print(new_url_db, "< ----result new url")
#     parsed_url = urlparse(x)
#     domain = parsed_url.netloc
#     print(domain, "< ---- domain is created")

#     # path = parsed_url.path

#     hashids = Hashids(min_length=8, salt="your_salt_here")

#     # Кодирование
#     # original_string = url
#     # hashed_id = hashids.encode_hex(original_string.encode().hex())
#     # print(f"Hashed: {hashed_id}")

#     # Декодирование
#     # decoded = bytes.fromhex(hashids.decode_hex(hashed_id)).decode()
#     # print(f"Decoded: {decoded}")


def index(request, url=None):
    print(url)
    # create(url)
    return render(request, "index.html", {"test": True})


# Create your views here.
