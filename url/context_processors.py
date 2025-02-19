from .models import Handler
from django.contrib import messages


def my_list_urls(request):
    """
    Получить все короткие Url
    Глобальная видимость контекста
    """

    try:
        my_list = Handler.objects.all()
        return {"my_list": my_list}
    except Exception as e:
        print(e)
        messages.success(request, "Что-то не так")
