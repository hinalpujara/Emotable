from django.urls import path, re_path
# from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/(?P<post_id>\w+)/', consumers.ChatConsumer.as_asgi()),
]