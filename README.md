[![Lint](https://github.com/Krd2024/url_short/actions/workflows/lint.yml/badge.svg)](https://github.com/Krd2024/url_short/actions/workflows/lint.yml)
# url_short
![2025-02-19_22-54-42](https://github.com/user-attachments/assets/fc73cdf5-bd8a-4c24-ab02-3c3c5f99d14a)



## Описание проекта

URL Shortener — это веб-приложение для сокращения длинных URL-адресов с возможностью добавления описаний для удобства управления ссылками. Все созданные ссылки сохраняются в базе данных, что позволяет просматривать их в удобном формате, управлять ими и быстро переходить по сокращенным адресам.

## Функционал

1. **Сокращение URL-адресов**:
   - Пользователь вводит длинный URL, который автоматически преобразуется в короткий адрес.
   - Дополнительно к короткому, можно указать желаемый адрес.

2. **Добавление описания**:
   - К каждой ссылке можно добавить описание, позволяющее пользователю легче идентифицировать назначение ссылки.

3. **Сохранение данных в базе данных**:
   - Оригинальный URL, сокращенная ссылка и описание сохраняются в базе данных для последующего использования и управления.

4. **Просмотр и управление ссылками**:
   - На главной странице отображается таблица всех созданных ссылок, которая содержит:
     - Оригинальный URL.
     - Кастомный URL.
     - Сокращенный URL.
     - Описание.
   - В таблице можно удалять ссылки с описанием по мере необходимости.

5. **Переход по сокращенному URL**:
   - Есть отдельное поле для ввода короткой ссылки, позволяющее перейти на соответствующий оригинальный URL.


## Используемые технологии

- **Backend**: Python (Django)
- **Frontend**: HTML, CSS, JavaScript
- **База данных**: SQLite

## Запуск проекта


1.Склонируйте репозиторий:
   ```bash
git clone https://github.com/Krd2024/url_short.git
```
2.Создание виртуального окружения
```bash
python -m venv .venv
```
3.Активация виртуального окружения
```bash
.venv\Scripts\activate
```
4.Установка зависимостей проекта
```bash
pip install -r req.txt
```
**Сгенерировать SECRET_KEY в Django**
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```
**Создать файл .env**
Добавьте соответствующие значения в .env файл:
```python
SECRET_KEY = см. выше
```
5.Миграции
```bash
python manage.py migrate
```
6.Запуск
```bash
python manage.py runserver
```



