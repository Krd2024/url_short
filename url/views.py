from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render
from url.models import Handler
import json


def custom_url_validator(value):
    if not value.startswith("http://") and not value.startswith("https://"):
        print("URL должен начинаться с http:// или https://")
        return False

    else:
        print("Всё нормально")
        return True


@csrf_exempt
def shorten_url(request):
    """Запись в БД полный Url и возврат сокращенного"""

    if request.method == "POST":
        # my_view(request)
        try:
            data = json.loads(request.body)
            url = data.get("url")
            url_descrip = data.get("urlDescrip")
            print(url_descrip)

            if not custom_url_validator(url):
                return JsonResponse({"error": "Неверный формат данных"}, status=400)

            new_url_db = Handler(url=url, discription=url_descrip)
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
        # my_view(request)
        try:
            data = json.loads(request.body)
            short_url = data.get("shortUrl_go")
            # Получить токен адреса
            token_url = short_url.split("/")
            print(token_url[1], "< ---- token")
            try:
                real_url = Handler.objects.get(token=token_url[1])
                print(f"{real_url.url} - полный Url для {short_url}")
                # fetch_and_parse_page(request, real_url.url)
                return JsonResponse(
                    {
                        "url": real_url.url,
                    }
                )
            except Handler.DoesNotExist:
                print("Нет соответствующей записи")
        except Exception as e:
            print(e)

        except json.JSONDecodeError:
            print("error: Неверный формат данных")
        #     return JsonResponse({"error": "Неверный формат данных"}, status=400)

    return JsonResponse({"error": "Нет соответствующей записи"}, status=405)


def url_delete(request, id):
    if request.method in ["POST", "DELETE"]:
        print(id, "< ---------")
        url_instance = get_object_or_404(Handler, id=id)
        url_instance.delete()
        return JsonResponse({"success": True, "message": "URL успешно удалён"})

    return JsonResponse(
        {"success": False, "message": "Неподдерживаемый метод запроса"}, status=405
    )


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
