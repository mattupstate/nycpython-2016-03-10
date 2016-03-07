===========
Rittenhouse
===========

In days of yore, implemeting asynchronous code with Python usually meant using
something like `gevent`_, `Twisted`_, or `Tornado`_. These are all fantastic
tools, but Python 3 now supports native coroutines via `asyncio`_. Additionally,
there are a growing number of libraries that take advantage of this feature. As
such, it is now posisble to implement such things as the `Websocket Protocol`_
without the aforementioned tools.

Rittenhouse is meant to serve as an illustration of how one might build a basic
web application that offers a Websocket interface using `aiohttp`_. Please note
that at the time this was developed this library was still very new and in
active development.

This application was originally developed for a presentation given at an NYC
Python `meetup`_ on March 10th, 2016.

Prerequisites
=============

Before getting started, please install `VirtualBox`_, `Docker`_ and `Compose`_.
This is to provide a predictable and repeatable local development environment.

Quick Start(s)
==============

Ensure the Docker machine is running::

    $ eval "$(make machine)"

To run the application::

    $ make server

To view the application logs::

    $ docker-compose logs web

When you do not care to work with this project anymore you may want to stop
the Docker machine::

    $ make stop

.. _gevent: http://www.gevent.org/
.. _Twisted: https://twistedmatrix.com/
.. _Tornado: http://www.tornadoweb.org/
.. _asyncio: https://docs.python.org/3/library/asyncio.html
.. _aiohttp: http://aiohttp.readthedocs.org/
.. _meetup: www.meetup.com/nycpython/events/228922678/
.. _Websocket Protocol: https://tools.ietf.org/html/rfc6455
.. _VirtualBox: https://www.virtualbox.org/
.. _Docker: https://www.docker.com/
.. _Compose: https://github.com/docker/compose
