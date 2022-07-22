"""
ASGI config for app project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url
from djangochannelsrestframework.consumers import view_as_consumer



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

#application = get_asgi_application()
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            #re_path(r"ws/$", PoolsConsumer.as_asgi()),

        ])
    ),
    # Just HTTP for now. (We can add other protocols later.)
})

