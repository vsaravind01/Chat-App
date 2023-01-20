import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from .models import Room, Message
from datetime import datetime


class ChatConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room = None
        self.room_name = None
        self.room_group_name = None

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        try:
            self.room = Room.objects.get(name__exact=self.room_name)
        except:
            self.close()

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user = self.scope["user"].username

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user,
                'time': datetime.now().isoformat()
            }
        )

        Message.objects.create(msg=message, user=user, room=self.room)

    def chat_message(self, event):
        self.send(text_data=json.dumps({
            'type': event['type'],
            'message': event['message'],
            'user': event['user'],
            'time': event['time']
        }))
