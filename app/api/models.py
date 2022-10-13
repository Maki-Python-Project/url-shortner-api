from django.db import models


class UrlShortener(models.Model):
    user_ip_address = models.GenericIPAddressField(default='0.0.0.0')
    longurl = models.CharField(max_length=255)
    shorturl = models.SlugField(max_length=8)

    def __str__(self) -> str:
        return self.shorturl
