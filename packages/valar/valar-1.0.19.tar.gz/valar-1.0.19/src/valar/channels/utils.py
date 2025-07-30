import asyncio

import importlib
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings




async def execute_channel(method, data, sender):
    thread = asyncio.to_thread(method,  data, sender)
    asyncio.create_task(thread)



def channel_wrapper(func):
    def wrapper(*args, **kwargs):
        data, sender = args
        sender.to_clients(None, [sender.client],'start')
        result = func(*args, **kwargs)
        sender.to_clients(None, [sender.client], 'stop')
        return result
    return wrapper


def get_channel_handler(handler):
    try:
        root = settings.VALAR_CHANNEL_HANDLER_MAPPING
        path, name = root.rsplit(".", 1)
    except (ValueError, AttributeError):
        raise ImproperlyConfigured("Cannot find VALAR_CHANNEL_HANDLER_MAPPING setting.")
    try:
        module = importlib.import_module(path)
        mapping = getattr(module, name)
    except ImportError:
        raise ImproperlyConfigured("Cannot import VALAR_CHANNEL_HANDLER_MAPPING module %r" % path)
    except AttributeError:
        raise ImproperlyConfigured("module %r has no attribute %r" % (path, name))
    try:
        method = mapping[handler]
    except KeyError:
        raise ImproperlyConfigured("Cannot find handler in %r" % root)
    return method