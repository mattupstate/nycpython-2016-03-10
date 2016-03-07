# -*- coding: utf-8 -*-
"""
    rittenhouse.resources.instance
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Object instance resources
"""

from aiohttp.web import Response, json_response

from rittenhouse.persistence import ObjectNotFoundError
from rittenhouse.resources.utils import halify_object


def get_object(fn):
    async def _get_object(request):
        uuid = request.match_info['uuid']

        try:
            obj = await request.app.repository.find(uuid)
        except ObjectNotFoundError:
            return json_response({'message': 'Not found'}, status=404)

        return await fn(request, obj)

    return _get_object


@get_object
async def get(request, obj):
    return json_response(halify_object(obj))


@get_object
async def post(request, obj):
    message = await request.json()

    request.app.broadcast('object-message', {
        'message': message,
        'object': obj
    })

    return Response(status=204)
