import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import mentalhealthapp.routing  # Replace with your app name

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mentalhealthapp.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(mentalhealthapp.routing.websocket_urlpatterns)
    ),
})
