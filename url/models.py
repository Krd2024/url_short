from django.contrib.auth.models import AbstractUser
from django.forms import ValidationError
from urllib.parse import urlparse
from django.db import models
from hashids import Hashids
from loguru import logger

# from django.core.validators import URLValidator
# import hashlib


def custom_url_validator(value):
    """Валидатор URL"""

    if not value.startswith("http://") and not value.startswith("https://"):
        print("URL должен начинаться с http:// или https://")
        raise ValidationError("URL должен начинаться с http:// или https://")


# Create your models here.
class User(AbstractUser):
    pass


class Handler(models.Model):
    url = models.URLField(unique=True)
    token = models.CharField(max_length=20)
    new_url = models.CharField(max_length=50, blank=True, null=True)
    castom_url = models.CharField(max_length=50, blank=True, null=True)
    discription = models.CharField(max_length=200, blank=True)

    def generate_token(self):
        """Создать токен для Url"""

        parsed_url = urlparse(self.url)
        path = parsed_url.path
        hashids = Hashids(min_length=8, salt="your_salt_here")
        return hashids.encode_hex(path.encode().hex())[:12]

    def new_url_generator(self):
        """Сформировать новый Url"""

        domain = urlparse(self.url).netloc
        logger.debug(domain)
        return f"https://{domain}/{self.token}"

    def save(self, *args, **kwargs):
        """Генерируем токен"""

        if not self.token:
            self.token = self.generate_token()
        self.new_url = self.new_url_generator()
        super().save(*args, **kwargs)
