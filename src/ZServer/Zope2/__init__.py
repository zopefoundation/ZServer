##############################################################################
#
# Copyright (c) 2001, 2002 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Zope application package."""

import os

from ZServer.Zope2.Startup.run import configure

_began_startup = 0


def startup():
    """Initialize the Zope Package and provide a published module"""
    global _began_startup
    if _began_startup:
        # Already began (and maybe finished) startup, so don't run again
        return
    _began_startup = 1
    _configure()
    from Zope2.App.startup import startup as _startup
    _startup()


def app(*args, **kw):
    """Utility for scripts to open a connection to the database"""
    from Zope2 import bobo_application
    startup()
    return bobo_application(*args, **kw)


def debug(*args, **kw):
    """Utility to try a Zope request using the interactive interpreter"""
    startup()
    import ZPublisher
    return ZPublisher.test('Zope2', *args, **kw)


def _configure():
    configfile = os.environ.get('ZOPE_CONFIG')
    if configfile is not None:
        configure(configfile)
