from channels.generic.websocket import WebsocketConsumer
import json

class MyWebsocket(WebsocketConsumer):
  def connect(self):
    self.accept()
    from .models import Message
    all_message = Message.objects.all()
    text_messages = [mes.text for mes in all_message]
    self.send(text_data=json.dumps({
            'response': text_messages
        }))
  

  def receive(self, text_data):
    
    from .models import Message
    data = json.loads(text_data)
    msg = data.get("message" ,'')
    Message.objects.create(text = msg)

    all_message = Message.objects.all()
    text_messages = [mes.text for mes in all_message]
    self.send(text_data=json.dumps({
            'response': text_messages
        }))
    
  def disconnect(self , code):
    print("disconnected")

       