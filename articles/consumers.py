import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ArticleConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("articles", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("articles", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        # (pas nécessaire côté client dans notre cas)

    async def article_posted(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"]
        }))
