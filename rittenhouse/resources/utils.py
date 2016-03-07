# -*- coding: utf-8 -*-
"""
    rittenhouse.resources.utils
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Resource utilities
"""

def halify_object(obj):
    meta = {
        '_links': {
            'self': {
                'href': '/objects/%s' % obj['uuid']
            }
        }
    }
    return {**meta, **obj}
