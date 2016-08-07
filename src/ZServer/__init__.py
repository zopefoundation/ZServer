##############################################################################
#
# Copyright (c) 2002 Zope Foundation and Contributors.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

from __future__ import absolute_import

from zope.deferredimport import deprecated

from ZServer import utils

# BBB
deprecated(
    'Please import from ZServer.medusa',
    resolver='ZServer.medusa:resolver',
    logger='ZServer.medusa:logger')

deprecated(
    'Please import from ZServer.medusa.monitor',
    secure_monitor_server='ZServer.medusa.monitor:secure_monitor_server')

deprecated(
    'Please import from ZServer.utils',
    requestCloseOnExec='ZServer.utils:requestCloseOnExec')

deprecated(
    'Please import from ZServer.FCGIServer',
    FCGIServer='ZServer.FCGIServer:FCGIServer')

deprecated(
    'Please import from ZServer.FTPServer',
    FTPServer='ZServer.FCGIServer:FTPServer')

deprecated(
    'Please import from ZServer.HTTPServer',
    zhttp_handler='ZServer.HTTPServer:zhttp_handler',
    zhttp_server='ZServer.HTTPServer:zhttp_server')

deprecated(
    'Please import from ZServer.PCGIServer',
    PCGIServer='ZServer.PCGIServer:PCGIServer')

deprecated(
    'Please import from ZServer.Zope2.Startup.config.',
    CONNECTION_LIMIT='ZServer.Zope2.Startup.config:ZSERVER_CONNECTION_LIMIT',
    exit_code='ZServer.Zope2.Startup.config:ZSERVER_EXIT_CODE',
    LARGE_FILE_THRESHOLD=('ZServer.Zope2.Startup.config:'
                          'ZSERVER_LARGE_FILE_THRESHOLD'),
    setNumberOfThreads='ZServer.Zope2.Startup.config:setNumberOfThreads',
)

# the ZServer version number
ZSERVER_VERSION = '1.1'

# the Zope version string
ZOPE_VERSION = utils.getZopeVersion()

# we need to patch asyncore's dispatcher class with a new
# log_info method so we see medusa messages in the zLOG log
utils.patchAsyncoreLogger()

# we need to patch the 'service name' of the medusa syslog logger
utils.patchSyslogServiceName()
