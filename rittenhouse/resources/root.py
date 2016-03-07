# -*- coding: utf-8 -*-
"""
    rittenhouse.resources.root
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Root resource
"""

from aiohttp.web import json_response
from aiohttp_jinja2 import render_template


def get(request):
    if 'application/hal+json' in request.headers['ACCEPT']:
        return json_response({
            '_links': {
                'self': {
                    'href': '/'
                },
                'objects': {
                    'href': '/objects'
                },
                'object': {
                    'href': '/objects/{uuid}',
                    'templated': True
                }
            }
        })

    return render_template('index.html', request, {})
