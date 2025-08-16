from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
  re_path('chat_ws/' , consumers.MyWebsocket.as_asgi()  )
]