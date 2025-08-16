from django.urls import path
from . import consumers

websocket_urlpatterns = [
  path('chat_ws/' , consumers.MyWebsocket.as_asgi()  )
]