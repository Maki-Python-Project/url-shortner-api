import pytest

from rest_framework import status
from django.conf import settings

from .models import UrlShortener
from .service import create_shortner_url


@pytest.mark.django_db
def test_create_url_obj(create_longurl_and_shorturl):
    longurl, shorturl = create_longurl_and_shorturl
    UrlShortener.objects.create(
        longurl=longurl, shorturl=shorturl
    )

    assert UrlShortener.objects.all().count() == 1, 'UrlShortener object was not created'


@pytest.mark.django_db
def test_redirect(api_client, create_longurl_and_shorturl):
    longurl, hash = create_longurl_and_shorturl
    url = create_shortner_url(longurl, hash)[1]
    response = api_client.get(url)

    assert response.status_code == status.HTTP_302_FOUND, 'Cannot redirect shortener url'


@pytest.mark.django_db
def test_check_status_code_of_count_all_urls(api_client):
    url = settings.HOST_URL + 'shortened-urls-count/'
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK, 'Page not found'


@pytest.mark.django_db
def test_check_count_all_urls(api_client, create_longurl_and_shorturl):
    url = settings.HOST_URL + 'shortened-urls-count/'
    longurl, shorturl = create_longurl_and_shorturl
    UrlShortener.objects.create(
        longurl=longurl, shorturl=shorturl
    )
    response = api_client.get(url)

    assert response.json()['count'] > 0, 'Count of URLs less than 1'


@pytest.mark.django_db
def test_create_shortener_url(api_client, create_longurl_and_shorturl):
    url = settings.HOST_URL + 'shorten/'
    response = api_client.post(url, {
        'longurl': create_longurl_and_shorturl[1]
    })

    assert response.status_code == status.HTTP_200_OK, 'Cannot create shortener url'
