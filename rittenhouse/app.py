# -*- coding: utf-8 -*-
"""
    rittenhouse.app
    ~~~~~~~~~~~~~~~

    App module
"""

import asyncio
import json
import logging
import os

from datetime import datetime

import aiohttp_debugtoolbar
import aiohttp_jinja2
import jinja2

from aiohttp import MsgType
from aiohttp.web import Application, WebSocketResponse

from rittenhouse import config, persistence, resources

logger = logging.getLogger(__name__)


def _get_directory(name):
    basedir = os.path.dirname(__file__)
    return os.path.join(basedir, name)


class Websocket(object):

    def __init__(self, response):
        self._response = response
        self._created_at = datetime.utcnow()

    @property
    def response(self):
        return self._response

    @property
    def created_at(self):
        return self._created_at

    def __str__(self):
        return "<Websocket created_at=%s>" % self.created_at.isoformat()


class Rittenhouse(Application):

    _websockets = []

    def __init__(self, repository, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.repository = repository

        self._register_handlers()
        self._register_static()
        self._register_templates()

        if config.DEBUG:
            aiohttp_debugtoolbar.setup(self)

        self.on_shutdown.append(self.close)

    def _register_handlers(self):
        for method, url, handler in [
            ('GET', '/', resources.root.get),
            ('GET', '/objects', resources.collection.get),
            ('POST', '/objects', resources.collection.post),
            ('GET', '/objects/{uuid}', resources.instance.get),
            ('POST', '/objects/{uuid}', resources.instance.post),
        ]:
            self.router.add_route(method, url, handler)

    def _register_static(self):
        self.router.add_static('/static', _get_directory('static'))

    def _register_templates(self):
        loader = jinja2.FileSystemLoader(_get_directory('templates'))
        aiohttp_jinja2.setup(self, loader=loader)

    async def create_websocket(self, request):
        """Starts a websocket connection and holds on until the client
        disconnects.

        :param  request: the originating request object
        """
        response = WebSocketResponse()
        await response.prepare(request)

        websocket = Websocket(response)
        self._websockets.append(websocket)
        logger.info('registered websocket %s', websocket)

        async for msg in response:
            if msg.tp != MsgType.text:
                break

        self._websockets.remove(websocket)

        await response.close()
        logger.info('closed websocket %s', websocket)
        return response

    def broadcast_event(self, event, payload):
        """Broadcasts an event with a specified payload to all open websocket
        connections.

        :param  event: the name of the event
        :param  payload: a payload object to add to the event object
        """
        message = json.dumps({
            'event': event,
            'payload': payload
        })

        async def _send_str(ws):
            ws.response.send_str(message)
            logger.debug('message sent to %s', ws)

        coroutine = asyncio.gather(*[
            _send_str(ws)
            for ws in self._websockets
        ], loop=self.loop)

        logger.info('broadcasting %s to %s websockets',
                     message, len(self._websockets))

        asyncio.ensure_future(coroutine, loop=self.loop)

    async def create_object(self):
        """Returns a new object and broadcasts an event to all currently open
        websocket connections.
        """
        obj = await self.repository.new()
        self.broadcast_object_created(obj)
        return obj

    async def get_all_objects(self):
        """Returns a list of all persited objects.
        """
        return await self.repository.find_all()

    async def get_object(self, uuid):
        """Returns an object with the specified uuid.

        :param  uuid: an object uuid
        """
        return await self.repository.find(uuid)

    def broadcast_object_created(self, obj):
        """Broadcasts an `object-created` event to all currently open websocket
        connections.

        :param  obj: the object that was created
        """
        self.broadcast_event('object-created', {
            'object': obj
        })

    def broadcast_object_message(self, obj, message):
        """Broadcasts an `object-message` event to all currently open websocket
        connections.

        :param  obj: the object for which the event relates to
        :param  message: the event message
        """
        self.broadcast_event('object-message', {
            'object': obj,
            'message': message
        })

    async def close(self, app=None):
        """Closes all open websocket connections.
        """
        async def _close_websocket(ws):
            await ws.response.close(message='Server shutdown')
            logger.debug('websocket %s successfully closed', ws)

        logger.info('closing %s open websockets', len(self._websockets))

        await asyncio.gather(*[
            _close_websocket(ws)
            for ws in self._websockets
        ], loop=self.loop)

        logger.info('websocket shutdown completed')


