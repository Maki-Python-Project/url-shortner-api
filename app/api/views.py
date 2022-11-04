from typing import Type
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.db.models import Count
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.views import View
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views.decorators.vary import vary_on_cookie
from rest_framework import generics
from rest_framework.response import Response

from api.models import UrlShortener
from api.serializers import UrlShortenerSerializer
from api.utils import get_short_url, get_user_ip


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class MakeshortUrl(generics.CreateAPIView):
    serializer_class = UrlShortenerSerializer

    @method_decorator(cache_page(CACHE_TTL))
    def post(self, request: Response) -> Response:
        longurl = request.data.get('longurl')

        ip = get_user_ip(request)

        long_url_obj = UrlShortener.objects.filter(longurl=longurl, user_ip_address=ip)
        if long_url_obj.exists():
            long_url_obj = long_url_obj.get()
            return Response({'longurl': long_url_obj.longurl, 'shorturl': settings.HOST_URL + long_url_obj.shorturl})

        shorturl = get_short_url()

        url_pair = UrlShortener()
        url_pair.longurl = longurl
        url_pair.shorturl = shorturl
        url_pair.user_ip_address = ip
        url_pair.save()
        shorturl = settings.HOST_URL + shorturl

        return Response({'longurl': longurl, 'shorturl': shorturl})


class RedirectUrl(View):
    # @method_decorator(cache_page(CACHE_TTL))
    def get(self, request: Response, shorturl: str) -> HttpResponseRedirect:
        redirect_link = UrlShortener.objects.filter(shorturl=shorturl).values('longurl').first()['longurl']
        return redirect(redirect_link)


class TheMostPopularUrl(generics.ListAPIView):
    serializer_class = UrlShortenerSerializer

    def get_queryset(self) -> UrlShortener:
        return UrlShortener.objects.values("longurl").annotate(count=Count('longurl')).order_by("-count")

    @method_decorator(vary_on_cookie)
    @method_decorator(cache_page(CACHE_TTL))
    def dispatch(self, *args, **kwargs):
        return super(TheMostPopularUrl, self).dispatch(*args, **kwargs)


@cache_page(CACHE_TTL)
def get_count_all_shortened_url(request: Response) -> JsonResponse:
    data = UrlShortener.objects.all().count()
    return JsonResponse({'count': data})
