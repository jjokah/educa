import json
from django.utils import timezone
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for handling real-time chat functionality.
    Manages connections, message sending/receiving for course-specific chat rooms.
    """

    async def connect(self):
        """
        Handles new WebSocket connections
        """
        # get user and create course-specific group
        self.user = self.scope['user']
        self.id = self.scope['url_route']['kwargs']['course_id']
        self.room_group_name = f'chat_{self.id}'
        # join room group - add user to group
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        # accept connection
        await self.accept()

    async def disconnect(self, close_code):
        """
        Handles WebSocket disconnection
        """
        # leave room group - remove user from group
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    async def receive(self, text_data):
        """
        Handles incoming messages from WebSocket.
        Broadcasts the message to all members in the room group.
        """
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        now = timezone.now()
        # broadcast message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.user.username,
                'datetime': now.isoformat(),
            }
        )

    async def chat_message(self, event):
        """
        Handles chat messages received from room group.
        """
        # send message to WebSocket
        await self.send(text_data=json.dumps(event))
    