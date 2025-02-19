from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render
from loguru import logger
from url.models import Handler
import json

from url.sirvices.verifications import check_short_url


def custom_url_validator(value):
    if not value.startswith("https://"):
        logger.debug(value)
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
            # Загружает JSON данные из тела запроса
            data = json.loads(request.body)
            url = data.get("url")  # Оригинальный URL
            url_descrip = data.get("urlDescrip")  # Описание URL
            url_castom = data.get("urlCastom")  # Кастомный URL (если есть)

            logger.debug(data)
            # Проверить корректность URL
            if not custom_url_validator(url):
                return JsonResponse({"error": "Неверный формат данных"}, status=400)
            # Проверить, был ли передан кастомный URL
            if len(url_castom.split()) > 0:
                # Проверить, существует ли уже такой кастомный URL в БД
                if Handler.objects.filter(castom_url=url_castom).exists():
                    logger.debug("Такой URL уже есть")
                    return JsonResponse(
                        {"error": "Такой кастомный URL уже есть"}, status=400
                    )
                else:
                    # Создать новую запись с кастомным URL
                    new_url_db = Handler(
                        url=url,
                        castom_url=f"https://{url_castom}",
                        discription=url_descrip,
                    )
                    new_url_db.save()  # Сохранить созданный кастомный URL
                    # В шаблоне показать кастомный
                    new_url = new_url_db.castom_url

            else:
                # Если кастомный URL не указан, создаём стандартный сокращённый URL
                # Стандартный сокращённый создаётся в любом случае (переопределен метод save())

                new_url_db = Handler(url=url, discription=url_descrip)
                new_url_db.save()
                # В шаблоне показать
                new_url = new_url_db.new_url

                logger.debug(new_url)

            # JSON-ответ с новым сокращённым URL
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
            short_url = Handler.objects.get(url=url)
            return JsonResponse({"shortUrl": short_url.new_url})

        except json.JSONDecodeError:
            logger.error("Неверный формат данных")
            return JsonResponse({"error": "Неверный формат данных"}, status=400)

    return JsonResponse({"error": "Метод не разрешен"}, status=405)


@csrf_exempt
def url_short_get(request):
    """
    Проверить и перейти по короткому URL

    """

    if request.method != "POST":
        return JsonResponse({"error": "Метод не поддерживается"}, status=405)

    try:
        # Загрузить JSON-данные из тела запроса
        data = json.loads(request.body)

        short_url = data.get("shortUrl_go")
        if not short_url:
            logger.error("Отсутствует URL")
            return JsonResponse({"error": "Отсутствует URL"}, status=400)

        logger.debug(f"Полученный URL: {short_url}")

        # Проверить наличие короткого или кастомного URL
        url_original = check_short_url(short_url)

        # Если есть, вернуть
        if url_original:
            return JsonResponse({"url": url_original})

        logger.error("Нет соответствующей записи")
        # Если нет, вернуть
        return JsonResponse({"error": "Нет соответствующей записи"}, status=404)

    except json.JSONDecodeError:
        logger.error("Ошибка декодирования JSON")
        return JsonResponse({"error": "Неверный формат данных"}, status=400)

    except KeyError:
        logger.error("Некорректный JSON-запрос")
        return JsonResponse({"error": "Некорректный JSON-запрос"}, status=400)

    except Exception as e:
        logger.exception(f"Неожиданная ошибка: {e}")
        return JsonResponse({"error": "Внутренняя ошибка сервера"}, status=500)


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
