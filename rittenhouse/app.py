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

        self.on_shutdown.append(self._close_all_websockets)

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

    async def _close_all_websockets(self, app):
        async def _close_webcosket(ws):
            await ws.close(message='Server shutdown')
            logger.debug('websocket %s successfully closed', ws)

        logger.info('closing %s open websockets', len(self._websockets))

        await asyncio.gather(*[
            _close_webcosket(ws)
            for ws in self._websockets
        ], loop=self.loop)

        logger.info('websocket shutdown completed')

    async def websocket(self, request):
        websocket = WebSocketResponse()
        await websocket.prepare(request)
        self._websockets.append(websocket)
        logger.info('registered websocket %s', websocket)

        async for msg in websocket:
            if msg.tp != MsgType.text:
                logger.debug('received nontext message from %s', websocket)
                break

        self._websockets.remove(websocket)
        await websocket.close()
        logger.info('closed websocket %s', websocket)

        return websocket

    def broadcast(self, event, payload):
        message = json.dumps({
            'event': event,
            'payload': payload
        })

        async def _send_str(ws):
            ws.send_str(message)
            logger.debug('message sent to %s', ws)

        coroutine = asyncio.gather(*[
            _send_str(ws)
            for ws in self._websockets
        ], loop=self.loop)

        logger.info('broadcasting %s to %s websockets',
                     message, len(self._websockets))

        asyncio.ensure_future(coroutine, loop=self.loop)

