# -*- coding: utf-8 -*-
"""
    rittenhouse.config
    ~~~~~~~~~~~~~~~~~~

    Config module
"""

import os


def _getenv(key, default):
    val = os.getenv(key)
    if not val:
        val = default
    else:
        clazz = default.__class__
        if clazz == bool:
            val = val.lower() in {'true', '1', 'yes'}
        else:
            val = clazz(val)
    return val


DEBUG = _getenv('DEBUG', False)
LOG_LEVEL = _getenv('LOG_LEVEL', 'WARN')
