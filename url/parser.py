from django.shortcuts import render
import requests
from bs4 import BeautifulSoup


def fetch_and_parse_page(request, url=None, **kwargs):
    url = "https://google.com"

    # Получаем HTML страницы
    response = requests.get(url)

    if response.status_code == 200:
        # Парсим HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Собираем стили из <link> и <style> тегов
        styles = ""

        # Парсим все <link> теги для внешних CSS
        for link in soup.find_all("link", {"rel": "stylesheet"}):
            css_url = link.get("href")
            if css_url:
                # Загружаем внешний CSS файл
                if css_url.startswith("http"):
                    css_response = requests.get(css_url)
                else:
                    # Если относительный путь, то добавляем домен
                    css_response = requests.get(url + css_url)

                if css_response.status_code == 200:
                    styles += css_response.text

        # Собираем inline-стили
        for style in soup.find_all("style"):
            styles += style.get_text()

        # Передаем HTML и стили в шаблон
        return render(
            request, "parser.html", {"html_content": soup.prettify(), "styles": styles}
        )

    return render(request, "parser.html", {"error": "Ошибка загрузки страницы."})
