##############################################################################
#
# Copyright (c) 2002 Zope Foundation and Contributors.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE
#
##############################################################################

from ZServer.PubCore import ZRendezvous

_handle = None


def handle(*args, **kw):
    global _handle

    if _handle is None:
        from ZServer.Zope2.Startup.config import ZSERVER_THREADS as _n
        _handle = ZRendezvous.ZRendevous(_n).handle

    return _handle(*args, **kw)
