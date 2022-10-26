import string
import random

from django.http import HttpRequest

from api.models import UrlShortener
from api.database import SessionLocal


def get_user_ip(request: HttpRequest) -> str:
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[-1].strip()
    else:
        return request.META.get('REMOTE_ADDR')


async def get_short_url() -> str:
    hash = string.ascii_uppercase + string.ascii_lowercase + string.digits
    shorturl = ''.join(random.sample(hash, 8))
    while True:
        has_to_continue = False
        async for obj in UrlShortener.objects.filter(shorturl=shorturl):
            shorturl = ''.join(random.sample(hash, 8))
            has_to_continue = True

        if not has_to_continue:
            break

    return shorturl


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()