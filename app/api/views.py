from api.apps import application
from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse
from rest_framework.response import Response
from django.db.models import Count
from django.http import HttpResponseRedirect
from typing import Type

from api.models import UrlShortener
from api.utils import get_user_ip, get_short_url


async def create_shorturl(request: Response) -> Response:
    longurl = request.POST.get('longurl')

    ip = get_user_ip(request)

    long_url_obj = UrlShortener.objects.filter(longurl=longurl, user_ip_address=ip)

    async for obj in long_url_obj:
        return JsonResponse({'longurl': obj.longurl, 'shorturl': settings.HOST_URL + obj.shorturl})

    shorturl = await get_short_url()

    await UrlShortener.objects.acreate(longurl=longurl, shorturl=shorturl, user_ip_address=ip)
    shorturl = settings.HOST_URL + str(shorturl)

    return JsonResponse({'longurl': longurl, 'shorturl': shorturl})


async def redirect_shorturl(request: Response, shorturl: str) -> HttpResponseRedirect:
    redirect_link = await UrlShortener.objects.filter(shorturl=shorturl).afirst()
    return redirect(redirect_link.longurl)


def get_the_most_popular(request) -> Type[UrlShortener]:
    qs = UrlShortener.objects.values("longurl").annotate(count=Count('longurl')).order_by('-count')
    return JsonResponse(list(qs), safe=False)


def get_count_all_shortened_url(request: Response) -> JsonResponse:
    data = UrlShortener.objects.all().count()
    return JsonResponse({'count': data})
