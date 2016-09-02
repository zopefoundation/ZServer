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

import os
import cStringIO
import tempfile
import unittest
import warnings

import ZConfig
import ZServer.Zope2.Startup
from ZServer.Zope2.Startup.options import ZopeOptions
import Products

TEMPNAME = tempfile.mktemp()
TEMPPRODUCTS = os.path.join(TEMPNAME, "Products")


def getSchema():
    startup = os.path.dirname(
        os.path.realpath(ZServer.Zope2.Startup.__file__))
    schemafile = os.path.join(startup, 'zopeschema.xml')
    opts = ZopeOptions()
    opts.schemafile = schemafile
    opts.load_schema()
    return opts.schema


class TestSchemaWarning(Warning):
    pass


class TestWarnFilter(unittest.TestCase):

    schema = None

    def setUp(self):
        if self.schema is None:
            TestWarnFilter.schema = getSchema()
        # There is no official API to restore warning filters to a previous
        # state.  Here we cheat.
        self.original_warning_filters = warnings.filters[:]

    def tearDown(self):
        warnings.filters[:] = self.original_warning_filters
        Products.__path__ = [d for d in Products.__path__
                             if os.path.exists(d)]

    def load_config_text(self, text):
        # We have to create a directory of our own since the existence
        # of the directory is checked.  This handles this in a
        # platform-independent way.
        schema = self.schema
        sio = cStringIO.StringIO(
            text.replace("<<INSTANCE_HOME>>", TEMPNAME))
        os.mkdir(TEMPNAME)
        os.mkdir(TEMPPRODUCTS)
        try:
            conf, handler = ZConfig.loadConfigFile(schema, sio)
        finally:
            os.rmdir(TEMPPRODUCTS)
            os.rmdir(TEMPNAME)
        self.assertEqual(conf.instancehome, TEMPNAME)
        return conf, handler

    def _dowarning1(self):
        warnings.warn('This is only a test.', TestSchemaWarning)

    def _dowarning2(self):
        warnings.warn('This is another test.')

    def test_warn_action(self):
        self.assertRaises(ZConfig.ConfigurationSyntaxError,
                          self._badwarnaction)

    def _badwarnaction(self):
        conf, handler = self.load_config_text("""\
            instancehome <<INSTANCE_HOME>>
            <warnfilter>
               action wontwork
               category ZServer.Zope2.Startup.tests.test_schema.TestSchemaWarning
            </warnfilter>
            """)

    def test_warn_category(self):
        self.assertRaises(ZConfig.ConfigurationSyntaxError,
                          self._badwarncategory)

    def _badwarncategory(self):
        conf, handler = self.load_config_text("""\
            instancehome <<INSTANCE_HOME>>
            <warnfilter>
               action error
               category A.Module.That.Doesnt.Exist
            </warnfilter>
            """)
