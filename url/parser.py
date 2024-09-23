from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

# URL страницы, которую хотите спарсить
import requests
from bs4 import BeautifulSoup


def my_view(request):
    return render(request, "index_2.html", {"error": "Ошибка загрузки страницы."})


# print(request)
# url = "https://example.com"

# # Получаем страницу
# response = requests.get(url)

# # Проверяем, успешен ли запрос
# if response.status_code == 200:
#     # Парсим HTML
#     soup = BeautifulSoup(response.text, "html.parser")
#     print("RESPONSE = 1")

#     # Можно извлечь данные из soup, например, заголовок
#     title = soup.title.string if soup.title else "Без заголовка"
#     print("RESPONSE = 2")

#     # Передаем данные в шаблон

#     x = render(
#         request,
#         "index_2.html",
#         {
#             "title": title,
#             "page_content": soup,
#             "test": 2222222222222222,
#         },
#     )
#     print(x, "<-------------------", soup)
#     return x
# else:
# return render(request, "index_2.html", {"error": "Ошибка загрузки страницы."})
