# -*- coding: utf-8 -*-
"""
    rittenhouse.resources.utils
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Resource utilities
"""

import json

from aiohttp.web import json_response as _json_response


def _dumps(*args, **kwargs):
    return json.dumps(indent=2, *args, **kwargs)


def json_response(*args, **kwargs):
    return _json_response(dumps=_dumps, *args, **kwargs)


def halify_object(obj):
    meta = {
        '_links': {
            'self': {
                'href': '/objects/%s' % obj['uuid']
            }
        }
    }
    return {**meta, **obj}
