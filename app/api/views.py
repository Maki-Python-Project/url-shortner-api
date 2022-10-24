import random
import string

from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse
from rest_framework.response import Response
from django.db.models import Count
from django.http import HttpResponseRedirect
from typing import Type

from .models import UrlShortener


async def create_shorturl(request: Response) -> Response:
    hash = string.ascii_uppercase + string.ascii_lowercase + string.digits
    longurl = request.POST.get('longurl')
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')

    long_url_obj = UrlShortener.objects.filter(longurl=longurl, user_ip_address=ip)

    async for obj in long_url_obj:
        return JsonResponse({'longurl': obj.longurl, 'shorturl': settings.HOST_URL + obj.shorturl})

    shorturl = ''.join(random.sample(hash, 8))

    while True:
        has_to_continue = False
        async for obj in UrlShortener.objects.filter(shorturl=shorturl):
            shorturl = ''.join(random.sample(hash, 8))
            has_to_continue = True

        if not has_to_continue:
            break

    await UrlShortener.objects.acreate(longurl=longurl, shorturl=shorturl, user_ip_address=ip)
    shorturl = settings.HOST_URL + shorturl

    return JsonResponse({'longurl': longurl, 'shorturl': shorturl})


async def redirect_shorturl(request: Response, shorturl: str) -> HttpResponseRedirect:
    redirect_link = await UrlShortener.objects.filter(shorturl=shorturl).afirst()
    return redirect(redirect_link.longurl)


def get_the_most_popular(request) -> Type[UrlShortener]:
    qs = UrlShortener.objects.values("longurl").annotate(count=Count('longurl')).order_by('-count')
    return  JsonResponse(list(qs), safe=False)

 
def get_count_all_shortened_url(request: Response) -> JsonResponse:
    data = UrlShortener.objects.all().count()
    return JsonResponse({'count': data})
