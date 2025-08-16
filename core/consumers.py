from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Message

class MyWebsocket(AsyncWebsocketConsumer):
    async def connect(self):
        # Add this user to the "chat" group
        await self.channel_layer.group_add("chat", self.channel_name)
        await self.accept()

        # Send all previous messages to the user who just connected
        all_message = await self.get_all_messages()
        await self.send(text_data=json.dumps({
            'response': all_message
        }))

    async def disconnect(self, close_code):
        # Remove from group on disconnect
        await self.channel_layer.group_discard("chat", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        msg = data.get("message", '')

        # Save to database
        await self.save_message(msg)

        # Send the message to everyone in the group
        await self.channel_layer.group_send(
            "chat",
            {
                "type": "chat_message",
                "message": msg,
            }
        )

    async def chat_message(self, event):
        # When group sends a message, broadcast it to WebSocket
        all_message = await self.get_all_messages()
        await self.send(text_data=json.dumps({
            'response': all_message
        }))

    # Helper: get all messages
    @staticmethod
    async def get_all_messages():
        messages = Message.objects.all()
        return [mes.text for mes in messages]

    # Helper: save a message
    @staticmethod
    async def save_message(msg):
        Message.objects.create(text=msg)
