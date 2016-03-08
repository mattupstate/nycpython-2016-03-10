# -*- coding: utf-8 -*-
"""
    rittenhouse.resources.collection
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Object collection resources
"""

from aiohttp.web import Response

from rittenhouse.resources import utils


async def get(request):
    if utils.is_websocket_request(request):
        return await request.app.create_websocket(request)
    elif not utils.is_hal_request(request):
        return Response(body=b'Unacceptable', status=406)

    objects = await request.app.get_all_objects()

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
    if not utils.is_hal_request(request):
        return Response(body=b'Unacceptable', status=406)
    obj = await request.app.create_object()
    return utils.json_response(utils.halify_object(obj))
