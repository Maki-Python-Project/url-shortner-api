import string
import random

from django.http import HttpRequest

from api.models import UrlShortener


def get_user_ip(request: HttpRequest) -> str:
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[-1].strip()
    else:
        return request.META.get('REMOTE_ADDR')


def get_short_url():
    hash = string.ascii_uppercase + string.ascii_lowercase + string.digits
    shorturl = ''.join(random.sample(hash, 8))
    while UrlShortener.objects.filter(shorturl=shorturl).exists():
        shorturl = ''.join(random.sample(hash, 8))
    return shorturl
