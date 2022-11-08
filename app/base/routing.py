import api.routing

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket': URLRouter(
        api.routing.websocket_urlpatterns
    ),
})
