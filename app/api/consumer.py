from channels.generic.websocket import WebsocketConsumer


class Consumer(WebsocketConsumer):
    def receive(self, text_data):
        pass
