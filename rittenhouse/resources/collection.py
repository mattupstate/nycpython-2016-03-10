# -*- coding: utf-8 -*-
"""
    rittenhouse.resources.collection
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Object collection resources
"""

from aiohttp.web import json_response

from rittenhouse.resources.utils import halify_object


async def get(request):
    if 'Sec-WebSocket-Version' in request.headers:
        return await request.app.websocket(request)

    objects = await request.app.repository.find_all()

    return json_response({
        '_links': {
            'self': {
                'href': '/objects'
            }
        },
        'total': len(objects),
        '_embedded': {
            'items': [
                halify_object(obj)
                for obj in objects
            ]
        }
    })


async def post(request):
    obj = await request.app.repository.new()

    request.app.broadcast('object-created', {
        'object': obj
    })

    return json_response(halify_object(obj))
