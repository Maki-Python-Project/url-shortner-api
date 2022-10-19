import random
import string
from django.conf import settings

from django.shortcuts import redirect
from django.http import JsonResponse
from rest_framework.request import Request
from rest_framework.decorators import api_view
from django.http import HttpResponseRedirect
from pymongo import MongoClient

from .repository import MongoRepository
from .utils import convert_cursor_to_dict


client = MongoClient('mongodb://mongoadmin:mongoadmin@localhost:27017/')
db = client['url_test']
db_connection = MongoRepository(db)


@api_view(['POST'])
def create_short_url(request: Request) -> JsonResponse:
    hash = string.ascii_uppercase + string.ascii_lowercase + string.digits
    longurl = request.data.get('longurl')
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')

    long_url_obj = db_connection.get_one({'longurl': longurl, 'user_ip_address': ip})

    if long_url_obj is not None:
        return JsonResponse(
            {'longurl': long_url_obj['longurl'], 'shorturl': settings.HOST_URL + long_url_obj['shorturl']}
        )

    shorturl = ''.join(random.sample(hash, 8))
    while db_connection.get_one({'shorturl': shorturl}) is not None:
        shorturl = ''.join(random.sample(hash, 8))

    db_connection.add({'longurl': longurl, 'shorturl': shorturl, 'user_ip_address': ip})
    shorturl = settings.HOST_URL + shorturl

    return JsonResponse({'longurl': longurl, 'shorturl': shorturl})


@api_view(['GET'])
def redirect_shorturl(request: Request, shorturl) -> HttpResponseRedirect:
    redirect_link = db_connection.get_one({'shorturl': shorturl})
    return redirect(redirect_link['longurl'])


@api_view(['GET'])
def get_the_most_popular(request: Request) -> JsonResponse:
    data = db_connection.annotate({'$group': {'_id': '$longurl', 'count': {'$sum': 1}}}, {'$sort': {'count': -1}})
    return JsonResponse(convert_cursor_to_dict(data))


@api_view(['GET'])
def get_count_all_shortened_url(request: Request) -> JsonResponse:
    data = db_connection.count()
    return JsonResponse({'count': data})
