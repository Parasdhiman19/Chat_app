from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from .models import Message

class MyWebsocket(WebsocketConsumer):
    def connect(self):
        # Create / join a group (all users join same chat group)
        self.room_group_name = "chat_room"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

        # Send all old messages when user connects
        all_message = Message.objects.all()
        text_messages = [mes.text for mes in all_message]
        self.send(text_data=json.dumps({
            'response': text_messages
        }))

    def receive(self, text_data):
        data = json.loads(text_data)
        msg = data.get("message", "")

        # Save in DB
        Message.objects.create(text=msg)

        # Broadcast to everyone in the group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": msg
            }
        )

    def chat_message(self, event):
        msg = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            "response": msg
        }))

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
