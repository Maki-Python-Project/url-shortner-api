from rest_framework.serializers import ModelSerializer
from .models import UrlShortener


class UrlShortenerSerializer(ModelSerializer):
    class Meta:
        model = UrlShortener
        fields = ['longurl', 'shorturl']
