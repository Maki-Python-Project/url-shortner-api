from django.conf import settings

from .models import UrlShortener


def create_shortner_url(longurl, shorturl):
    UrlShortener.objects.create(
            longurl=longurl,
            shorturl=shorturl
        )
    longurl = longurl
    shorturl = settings.HOST_URL + shorturl
    return longurl, shorturl
