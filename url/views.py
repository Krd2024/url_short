from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render
from loguru import logger
from url.models import Handler
import json


def custom_url_validator(value):
    if not value.startswith("https://"):
        logger.error("URL должен начинаться с https://")
        return False
    else:
        logger.info("Всё нормально c URL")
        return True


@csrf_exempt
def shorten_url(request):
    """Запись в БД полный Url и возврат сокращенного"""

    if request.method == "POST":
        try:

            data = json.loads(request.body)
            url = data.get("url")
            url_descrip = data.get("urlDescrip")
            url_castom = data.get("urlCastom")

            logger.debug(data)

            if not custom_url_validator(url):
                return JsonResponse({"error": "Неверный формат данных"}, status=400)

            if len(url_castom.split()) > 0:
                if Handler.objects.filter(castom_url=url_castom).exists():
                    logger.debug("Такой URL уже есть")
                    return JsonResponse(
                        {"error": "Такой кастомный URL уже есть"}, status=400
                    )
                else:
                    new_url_db = Handler(
                        url=url, castom_url=url_castom, discription=url_descrip
                    )
                    new_url_db.save()
                    new_url = "http://" + new_url_db.castom_url

            else:

                new_url_db = Handler(url=url, discription=url_descrip)
                new_url = new_url_db.new_url
                new_url_db.save()

            return JsonResponse(
                {
                    "message": "Сокращенный URL создан!",
                    "url": url,
                    "shortUrl": new_url,
                }
            )
        except IntegrityError:
            logger.error("Этот URL уже есть в сокращённом виде")
            # Если Url уже существует вернуть уже сформированный короткий Url
            url_obj = Handler.objects.get(url=url)
            return JsonResponse({"new_url": url_obj.new_url}, status=405)

        except json.JSONDecodeError:
            logger.error("Неверный формат данных")
            return JsonResponse({"error": "Неверный формат данных"}, status=400)

    return JsonResponse({"error": "Метод не разрешен"}, status=405)


@csrf_exempt
def url_short_get(request):
    """Проверить и перейти по короткому Url"""

    if request.method == "POST":
        # my_view(request)
        try:
            data = json.loads(request.body)
            short_url = data.get("shortUrl_go")

            # token_url = short_url.split("/")
            prefix, _, domain, token = short_url.split("/")
            real_url = Handler.objects.get(token=token)
            # logger.debug("//".join([prefix, domain]))
            if "//".join([prefix, domain]) != "/".join(real_url.url.split("/")[:3]):
                return JsonResponse({"error": "Неверный формат данных"}, status=400)

            logger.debug("/".join(real_url.url.split("/")[:3]))

            # logger.debug(token_url)
            # if prefix !
            # logger.debug((token_url[3], "< ---- token"))
            try:
                # real_url = Handler.objects.get(token=token_url[3])
                # print(f"{real_url.url} - полный Url для {short_url}")
                # fetch_and_parse_page(request, real_url.url)
                return JsonResponse(
                    {
                        "url": real_url.url,
                    }
                )
            except Handler.DoesNotExist:
                print("Нет соответствующей записи")

        except json.JSONDecodeError:
            print("error: Неверный формат данных")
            return JsonResponse({"error": "Неверный формат данных"}, status=400)
        except Exception as e:
            print(e)

        return JsonResponse({"error": str(e)}, status=405)


def url_delete(request, id):
    if request.method in ["POST", "DELETE"]:
        print(id, "< ---------")
        url_instance = get_object_or_404(Handler, id=id)
        url_instance.delete()
        return JsonResponse({"success": True, "message": "URL успешно удалён"})

    return JsonResponse(
        {"success": False, "message": "Неподдерживаемый метод запроса"}, status=405
    )


def index(request, url=None):
    print(url)
    # create(url)
    return render(request, "index.html", {"test": True})


# Create your views here.
