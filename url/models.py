from urllib.parse import urlparse
from django.db import models
from django.contrib.auth.models import AbstractUser
from hashids import Hashids


# Create your models here.
class User(AbstractUser): ...


class Handler(models.Model):
    url = models.URLField()
    token = models.CharField(max_length=20)
    new_url = models.CharField(
        max_length=255, blank=True, null=True
    )  # Поле для сохранения нового URL

    def generate_token(self):
        parsed_url = urlparse(self.url)
        path = parsed_url.path

        hashids = Hashids(min_length=8, salt="your_salt_here")
        return hashids.encode_hex(path.encode().hex())

    def new_url_generator(self):
        domain = urlparse(self.url).netloc
        print(domain, "< ---- domain")
        return f"{domain}/{self.token}"

    def save(self, *args, **kwargs):

        if not self.token:  # Генерируем токен только если его нет
            self.token = self.generate_token()
        self.new_url = self.new_url_generator()
        super().save(*args, **kwargs)
