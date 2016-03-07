# -*- coding: utf-8 -*-
"""
    rittenhouse.factory
    ~~~~~~~~~~~~~~~~~~~

    Factory method module
"""

from rittenhouse import app, persistence


def create_app(repository=None, loop=None):
    if repository is None:
        repository = create_repository()
    return app.Rittenhouse(repository, loop=loop)


def create_repository(datastore=None):
    if datastore is None:
        datastore = persistence.InMemoryDatastore()
    return persistence.ObjectRepository(datastore)
