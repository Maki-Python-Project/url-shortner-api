import pytest

from rest_framework import status
from django.conf import settings
from collections.abc import Callable

from .models import UrlShortener
from api.utils import get_db_connection


db_connection = get_db_connection()


@pytest.mark.django_db
def test_create_url_obj(create_longurl_and_shorturl: Callable) -> None:
    longurl, shorturl = create_longurl_and_shorturl
    db_connection.add({'longurl': longurl, 'shorturl': shorturl, 'user_ip_address': '127.0.0.0'}) 
    
    assert db_connection.count() >= 1, 'UrlShortener object was not created'

    db_connection.delete({'_id': db_connection.get_one({'shorturl': shorturl})['_id']})


@pytest.mark.django_db
def test_redirect(api_client: Callable, create_longurl_and_shorturl: Callable) -> None:
    longurl, hash = create_longurl_and_shorturl
    db_connection.add({'longurl': longurl, 'shorturl': hash, 'user_ip_address': '127.0.0.0'})
    longurl = longurl
    shorturl = settings.HOST_URL + hash
    response = api_client.get(shorturl)

    assert response.status_code == status.HTTP_302_FOUND, 'Cannot redirect shortener url'

    db_connection.delete({'_id': db_connection.get_one({'shorturl': hash})['_id']})


@pytest.mark.django_db
def test_check_status_code_of_count_all_urls(api_client: Callable) -> None:
    url = settings.HOST_URL + 'shortened-urls-count/'
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK, 'Page not found'


@pytest.mark.django_db
def test_check_count_all_urls(api_client: Callable, create_longurl_and_shorturl: Callable) -> None:
    url = settings.HOST_URL + 'shortened-urls-count/'
    longurl, shorturl = create_longurl_and_shorturl
    db_connection.add({'longurl': longurl, 'shorturl': shorturl, 'user_ip_address': '127.0.0.0'})
    response = api_client.get(url)

    assert response.json()['count'] > 0, 'Count of URLs less than 1'

    db_connection.delete({'_id': db_connection.get_one({'shorturl': shorturl})['_id']})


@pytest.mark.django_db
def test_create_shortener_url(api_client: Callable, create_longurl_and_shorturl: Callable) -> None:
    url = settings.HOST_URL + 'shorten/'
    longurl = create_longurl_and_shorturl[0]
    response = api_client.post(url, {
        'longurl': longurl,
        'user_ip_address': '127.0.0.0'
    })

    assert response.status_code == status.HTTP_200_OK, 'Cannot create shortener url'

    db_connection.delete({'_id': db_connection.get_one({'shorturl': response.json()['shorturl'][-8:]})['_id']})
