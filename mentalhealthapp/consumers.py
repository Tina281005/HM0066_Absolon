import json
from channels.generic.websocket import AsyncWebsocketConsumer

class VideoCallConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Accepts the WebSocket connection and assigns users to a room."""
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"video_call_{self.room_name}"

        # Add the WebSocket connection to the group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        """Removes the WebSocket connection from the group on disconnect."""
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """Handles incoming WebSocket messages."""
        data = json.loads(text_data)
        message_type = data.get("type")

        # Broadcast the message to the group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": message_type, "data": data}
        )

    async def video_signal(self, event):
        """Handles video call signaling (e.g., offer, answer, ICE candidates)."""
        await self.send(text_data=json.dumps(event["data"]))

    async def chat_message(self, event):
        """Handles chat messages in the video call."""
        await self.send(text_data=json.dumps(event["data"]))
