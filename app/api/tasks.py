import requests

from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from api.models import UrlShortener


channel_layer = get_channel_layer()


@shared_task
def get_joke():
    joke = UrlShortener.objects.order_by('?').first()
    async_to_sync(channel_layer.group_send)('api', {'type': 'send_jokes', 'text': joke.longurl})
