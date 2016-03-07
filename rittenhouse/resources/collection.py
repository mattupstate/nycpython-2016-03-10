# -*- coding: utf-8 -*-
"""
    rittenhouse.resources.collection
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Object collection resources
"""

from rittenhouse.resources import utils


async def get(request):
    if 'Sec-WebSocket-Version' in request.headers:
        return await request.app.websocket(request)

    objects = await request.app.repository.find_all()

    return utils.json_response({
        '_links': {
            'self': {
                'href': '/objects'
            }
        },
        'total': len(objects),
        '_embedded': {
            'items': [
                utils.halify_object(obj)
                for obj in objects
            ]
        }
    })


async def post(request):
    obj = await request.app.repository.new()

    request.app.broadcast('object-created', {
        'object': obj
    })

    return utils.json_response(utils.halify_object(obj))
