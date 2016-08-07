##############################################################################
#
# Copyright (c) 2003 Zope Foundation and Contributors.
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

from __future__ import absolute_import

import os
import cStringIO
import tempfile
import unittest

import ZConfig

import Products
from ZServer.Zope2.Startup import datatypes
from ZServer.Zope2.Startup.options import ZopeOptions

_SCHEMA = {}
TEMPNAME = tempfile.mktemp()
TEMPPRODUCTS = os.path.join(TEMPNAME, "Products")
TEMPVAR = os.path.join(TEMPNAME, "var")


def getSchema(schemafile):
    global _SCHEMA
    if schemafile not in _SCHEMA:
        opts = ZopeOptions()
        opts.schemafile = schemafile
        opts.load_schema()
        _SCHEMA[schemafile] = opts.schema
    return _SCHEMA[schemafile]


class ZServerStartupTestCase(unittest.TestCase):

    def tearDown(self):
        Products.__path__ = [d for d in Products.__path__
                             if os.path.exists(d)]

    @property
    def schema(self):
        return getSchema('zopeschema.xml')

    def load_config_text(self, text):
        # We have to create a directory of our own since the existence
        # of the directory is checked.  This handles this in a
        # platform-independent way.
        schema = self.schema
        sio = cStringIO.StringIO(
            text.replace("<<INSTANCE_HOME>>", TEMPNAME))
        os.mkdir(TEMPNAME)
        os.mkdir(TEMPPRODUCTS)
        os.mkdir(TEMPVAR)
        try:
            conf, handler = ZConfig.loadConfigFile(schema, sio)
        finally:
            os.rmdir(TEMPPRODUCTS)
            os.rmdir(TEMPVAR)
            os.rmdir(TEMPNAME)
        self.assertEqual(conf.instancehome, TEMPNAME)
        return conf, handler

    def test_cgi_environment(self):
        conf, handler = self.load_config_text("""\
            # instancehome is here since it's required
            instancehome <<INSTANCE_HOME>>
            <cgi-environment>
              HEADER value
              ANOTHER value2
            </cgi-environment>
            """)
        items = conf.cgi_environment.items()
        items.sort()
        self.assertEqual(
            items, [("ANOTHER", "value2"), ("HEADER", "value")])

    def test_ms_public_header(self):
        from ZServer.Zope2.Startup import config
        from ZServer.Zope2.Startup.handlers import handleConfig

        default_setting = config.ZSERVER_ENABLE_MS_PUBLIC_HEADER
        try:
            conf, handler = self.load_config_text("""\
                instancehome <<INSTANCE_HOME>>
                enable-ms-public-header true
                """)
            handleConfig(None, handler)
            self.assertTrue(config.ZSERVER_ENABLE_MS_PUBLIC_HEADER)

            conf, handler = self.load_config_text("""\
                instancehome <<INSTANCE_HOME>>
                enable-ms-public-header false
                """)
            handleConfig(None, handler)
            self.assertFalse(config.ZSERVER_ENABLE_MS_PUBLIC_HEADER)
        finally:
            config.ZSERVER_ENABLE_MS_PUBLIC_HEADER = default_setting

    def test_path(self):
        p1 = tempfile.mktemp()
        p2 = tempfile.mktemp()
        try:
            os.mkdir(p1)
            os.mkdir(p2)
            conf, handler = self.load_config_text("""\
                # instancehome is here since it's required
                instancehome <<INSTANCE_HOME>>
                path %s
                path %s
                """ % (p1, p2))
            items = conf.path
            self.assertEqual(items, [p1, p2])
        finally:
            if os.path.exists(p1):
                os.rmdir(p1)
            if os.path.exists(p2):
                os.rmdir(p2)

    def test_access_and_trace_logs(self):
        fn = tempfile.mktemp()
        conf, handler = self.load_config_text("""
            instancehome <<INSTANCE_HOME>>
            <logger access>
              <logfile>
                path %s
              </logfile>
            </logger>
            """ % fn)
        self.assert_(isinstance(conf.access, datatypes.LoggerFactory))
        self.assertEqual(conf.access.name, "access")
        self.assertEqual(conf.access.handler_factories[0].section.path, fn)
        self.assert_(conf.trace is None)
