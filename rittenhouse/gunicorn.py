# -*- coding: utf-8 -*-
"""
    rittenhouse.gunicorn
    ~~~~~~~~~~~~~~~~~~~~

    Gunicorn entrypoint
"""

import asyncio

from rittenhouse.factory import create_app

application = create_app(loop=asyncio.get_event_loop())
