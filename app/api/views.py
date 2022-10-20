from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse
from rest_framework.request import Request
from rest_framework.decorators import api_view
from django.http import HttpResponseRedirect

from api.utils import convert_cursor_to_dict, get_user_ip, get_short_url, get_db_connection


@api_view(['POST'])
def create_short_url(request: Request) -> JsonResponse:
    db_connection = get_db_connection()
    longurl = request.data.get('longurl')
    ip = get_user_ip(request)

    long_url_obj = db_connection.get_one({'longurl': longurl, 'user_ip_address': ip})

    if long_url_obj is not None:
        return JsonResponse(
            {'longurl': long_url_obj['longurl'], 'shorturl': settings.HOST_URL + long_url_obj['shorturl']}
        )

    shorturl = get_short_url(db_connection)

    db_connection.add({'longurl': longurl, 'shorturl': shorturl, 'user_ip_address': ip})
    shorturl = settings.HOST_URL + shorturl

    return JsonResponse({'longurl': longurl, 'shorturl': shorturl})


@api_view(['GET'])
def redirect_shorturl(request: Request, shorturl) -> HttpResponseRedirect:
    db_connection = get_db_connection()
    redirect_link = db_connection.get_one({'shorturl': shorturl})
    return redirect(redirect_link['longurl'])


@api_view(['GET'])
def get_the_most_popular(request: Request) -> JsonResponse:
    db_connection = get_db_connection()
    data = db_connection.annotate({'$group': {'_id': '$longurl', 'count': {'$sum': 1}}}, {'$sort': {'count': -1}})
    return JsonResponse(convert_cursor_to_dict(data))


@api_view(['GET'])
def get_count_all_shortened_url(request: Request) -> JsonResponse:
    db_connection = get_db_connection()
    data = db_connection.count()
    return JsonResponse({'count': data})
