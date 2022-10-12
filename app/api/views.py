import random
import string

from django.shortcuts import redirect
from django.views import View
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.response import Response
from django.db.models import Count

from .serializers import UrlShortenerSerializer
from .models import UrlShortener
from .service import create_shortner_url


class MakeshortUrl(generics.CreateAPIView):
    serializer_class = UrlShortenerSerializer

    def post(self, request):
        data = request.data
        hash = string.ascii_uppercase + string.ascii_lowercase + string.digits
        shorturl = (''.join(random.sample(hash, 8)))

        if UrlShortener.objects.filter(shorturl=shorturl).exists():
            longurl, shorturl = create_shortner_url(data['longurl'], shorturl)
            return Response({'longurl': longurl, 'shorturl': shorturl})

        longurl, shorturl = create_shortner_url(data['longurl'], shorturl)

        return Response({'longurl': longurl, 'shorturl': shorturl})


class RedirectUrl(View):
    def get(self, request, shorturl):
        redirect_link = UrlShortener.objects.filter(shorturl=shorturl).values('longurl').first()['longurl']
        return redirect(redirect_link)


class TheMostPopularUrl(generics.ListAPIView):
    serializer_class = UrlShortenerSerializer

    def get_queryset(self):
        return UrlShortener.objects.values("longurl").annotate(count=Count('longurl')).order_by("-count")


def get_count_all_shortened_url(request):
    data = UrlShortener.objects.all().count()
    return JsonResponse({'count': data})
