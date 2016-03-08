# -*- coding: utf-8 -*-
"""
    rittenhouse.resources.instance
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Object instance resources
"""

from aiohttp.web import Response

from rittenhouse.persistence import ObjectNotFoundError
from rittenhouse.resources import utils


def get_object_or_404(fn):
    async def _get_object(request):
        uuid = request.match_info['uuid']
        try:
            obj = await request.app.get_object(uuid)
        except ObjectNotFoundError:
            return utils.json_response({'message': 'Not found'}, status=404)
        return await fn(request, obj)
    return _get_object


@get_object_or_404
async def get(request, obj):
    if not utils.is_hal_request(request):
        return Response(body=b'Unacceptable', status=406)
    return utils.json_response(utils.halify_object(obj))


@get_object_or_404
async def post(request, obj):
    message = await request.json()
    request.app.broadcast_object_message(obj, message)
    return Response(status=204)
