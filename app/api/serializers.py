from rest_framework.serializers import ModelSerializer
from .models import UrlShortener


class UrlShortenerSerializer(ModelSerializer):
    class Meta:
        model = UrlShortener
        fields = ['longurl', 'shorturl', 'user_ip_address']
        read_only_fields = ['shorturl', 'user_ip_address']
