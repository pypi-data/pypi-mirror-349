import json

from .utils import execute_channel, get_channel_handler
from .. import ValarResponse
from ..channels import ValarSocketSender


async def handel_channel(request, handler):
    method = get_channel_handler(handler)
    body = json.loads(request.body)
    data = body.get('data')
    sender = ValarSocketSender(request)
    await execute_channel(method, data, sender)
    return ValarResponse(True)



