import json
from datetime import datetime

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from channels.generic.websocket import AsyncJsonWebsocketConsumer, JsonWebsocketConsumer
from django.conf import settings
from django.http import HttpRequest

try:
    GROUP = settings.VALAR_CHANNEL_GROUP_NAME
except AttributeError:
    GROUP = 'VALAR'

class ValarSocketSender:
    def __init__(self, request: HttpRequest):
        body = json.loads(request.body)
        client = request.headers.get('CLIENT')
        auth = request.headers.get('AUTH')
        uid = request.session.get('UID')
        if auth and not uid:
            raise Exception('Unauthorized!')
        self.client = client
        self.uid = uid
        self.handlerKey = body.get('handlerKey')
        self.channelKey = body.get('channelKey', 'default')
        self.send = get_channel_layer().group_send



    def __convert_body(self, emit, data, status ,clients = None, users = None):
        return {
            'type': emit,
            'data': {
                'status': status,
                'handlerKey': self.handlerKey,
                'channelKey': self.channelKey,
                'payload': data,
                'timestamp': datetime.now().timestamp()
            },
            'clients': clients or [],
            'users': users or [],
        }


    def to_users(self, data,  users, status='proceed'):
        body = self.__convert_body(emit='user.emit', data=data, status=status, users=users)
        async_to_sync(self.send)(GROUP, body)

    def to_clients(self,data, clients, status='proceed'):
        body = self.__convert_body(emit='client.emit', data=data, status=status, clients=clients)
        async_to_sync(self.send)(GROUP, body)


    def broadcast(self, data, status):
        body = self.__convert_body(emit='broadcast.emit', data=data, status=status)
        async_to_sync(self.send)(GROUP, body)

    def register(self):
        body = self.__convert_body(emit='register.emit',  data=None, status=None,clients=[self.client], users=[self.uid])
        async_to_sync(self.send)(GROUP, body)

class ValarConsumer(AsyncJsonWebsocketConsumer):

    def __init__(self):
        self.client = None
        self.uid = None
        super().__init__()

    async def connect(self):
        params = self.scope['url_route']['kwargs']
        self.client = params.get('client')
        await self.channel_layer.group_add(GROUP, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(GROUP, self.channel_name)
        await self.close(code)

    async def receive_json(self, data, *args, **kwargs):
        pass

    async def user_emit(self, event):
        users: list = event.get('users',[])
        data = event.get('data',{})
        if self.uid in users:
            await self.send_json(data)


    async def client_emit(self, event):
        clients: list = event.get('clients',[])
        data = event.get('data',{})
        if self.client in clients:
            await self.send_json(data)

    async def broadcast_emit(self, event):
        data = event.get('data',{})
        await self.send_json(data)

    async def register_emit(self, event):
        users: list = event.get('users', [])
        clients: list = event.get('clients',[])
        if self.client in clients:
            self.uid = users[0]


