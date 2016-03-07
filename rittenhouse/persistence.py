# -*- coding: utf-8 -*-
"""
    rittenhouse.persistence
    ~~~~~~~~~~~~~~~~~~~~~~~

    Persistence objects module
"""

from datetime import datetime
from typing import Optional, Sequence

from abc import ABCMeta, abstractmethod

import shortuuid


class ObjectNotFoundError(Exception):
    pass


class Datastore(metaclass=ABCMeta):

    @abstractmethod
    async def save(self, uuid, obj):
        pass

    @abstractmethod
    async def find(self, uuid):
        pass

    @abstractmethod
    async def find_all(self):
        pass


class InMemoryDatastore(Datastore):

    _objects = {}

    async def save(self, uuid, obj):
        self._objects[uuid] = obj

    async def find(self, uuid):
        return self._objects.get(uuid, None)

    async def find_all(self):
        return self._objects.values()


class ObjectRepository(object):

    def __init__(self, datastore):
        self._datastore = datastore

    def new(self):
        return self.save({
            'created_at': datetime.utcnow().isoformat()
        })

    async def save(self, obj):
        uuid = obj['uuid'] = shortuuid.uuid()
        await self._datastore.save(uuid, obj)
        return obj

    async def find(self, uuid):
        value = await self._datastore.find(uuid)
        if value is None:
            raise ObjectNotFoundError
        return value

    async def find_all(self):
        return await self._datastore.find_all()
