import random
import string
from django.conf import settings

from django.shortcuts import redirect
from django.views import View
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.response import Response
from django.db.models import Count
from pymongo import MongoClient

from .serializers import UrlShortenerSerializer
from .models import UrlShortener
from .repository import MongoRepository


client = MongoClient('mongodb://mongoadmin:mongoadmin@localhost:27017/')
db = client['url_test']
obj = MongoRepository(db)


class MakeshortUrl(generics.CreateAPIView):
    serializer_class = UrlShortenerSerializer

    def post(self, request):
        hash = string.ascii_uppercase + string.ascii_lowercase + string.digits
        longurl = request.data.get('longurl')
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')

        long_url_obj = UrlShortener.objects.filter(longurl=longurl, user_ip_address=ip)
        if long_url_obj.exists():
            long_url_obj = long_url_obj.get()
            return Response({'longurl': long_url_obj.longurl, 'shorturl': settings.HOST_URL + long_url_obj.shorturl})

        shorturl = ''.join(random.sample(hash, 8))
        while UrlShortener.objects.filter(shorturl=shorturl).exists():
            shorturl = ''.join(random.sample(hash, 8))

        url_pair = UrlShortener()
        url_pair.longurl = longurl
        url_pair.shorturl = shorturl
        url_pair.user_ip_address = ip
        url_pair.save()
        shorturl = settings.HOST_URL + shorturl

        return Response({'longurl': longurl, 'shorturl': shorturl})


class RedirectUrl(View):
    def get(self, request, shorturl):
        redirect_link = UrlShortener.objects.filter(shorturl=shorturl).values('longurl').first()['longurl']
        return redirect(redirect_link.longurl)


class TheMostPopularUrl(generics.ListAPIView):
    serializer_class = UrlShortenerSerializer

    def get_queryset(self):
        return UrlShortener.objects.values("longurl").annotate(count=Count('longurl')).order_by("-count")


def get_count_all_shortened_url(request):
    data = obj.count()
    return JsonResponse(data)
