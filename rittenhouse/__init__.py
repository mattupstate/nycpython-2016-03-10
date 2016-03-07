# -*- coding: utf-8 -*-
"""
    rittenhouse
    ~~~~~~~~~~~

    Rittenhouse application package
"""

import logging

from rittenhouse import config

logging.basicConfig(level='DEBUG' if config.DEBUG else config.LOG_LEVEL)
