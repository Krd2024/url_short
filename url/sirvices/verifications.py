from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from loguru import logger
from typing import Union


from url.models import Handler


def check_short_url(user_url: str) -> Union[str, bool]:
    """
    Проверяет наличие короткого или кастомного URL

    Первым вернёт кастомный
    Вторым вернёт сокращённый
    Вернёт False если нет введенного пользователем url

    """
    logger.info(user_url)
    user_url = user_url.strip()
    logger.info(user_url)
    try:
        url_query = Handler.objects.get(Q(castom_url=user_url) | Q(new_url=user_url))
        return url_query.url
    except ObjectDoesNotExist:
        return False
