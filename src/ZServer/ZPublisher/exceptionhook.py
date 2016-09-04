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
"""Initialize the Zope2 Package and provide a published module
"""

import logging
import sys

import AccessControl.User
from Acquisition import (
    aq_acquire,
    aq_base,
    aq_parent,
)
from Acquisition.interfaces import IAcquirer
from App.config import getConfiguration
import ExtensionClass
from six import reraise
from zExceptions import Redirect
from zExceptions import Unauthorized
from ZODB.POSException import ConflictError
from zope.component import queryMultiAdapter
from Zope2.App.startup import app, startup_time
from ZPublisher import Retry


class RequestContainer(ExtensionClass.Base):

    def __init__(self, r):
        self.REQUEST = r


class ExceptionHook(object):

    def __init__(self):
        self.conflict_errors = 0
        self.unresolved_conflict_errors = 0
        self.conflict_logger = logging.getLogger('ZPublisher.Conflict')
        self.error_message = 'standard_error_message'
        self.raise_error_message = 'raise_standardErrorMessage'

    def logConflicts(self, v, REQUEST):
        self.conflict_errors += 1
        level = getattr(getConfiguration(), 'conflict_error_log_level', 0)
        if not self.conflict_logger.isEnabledFor(level):
            return False
        self.conflict_logger.log(
            level,
            "%s at %s: %s (%d conflicts (%d unresolved) "
            "since startup at %s)",
            v.__class__.__name__,
            REQUEST.get('PATH_INFO', '<unknown>'),
            v,
            self.conflict_errors,
            self.unresolved_conflict_errors,
            startup_time)
        return True

    def __call__(self, published, REQUEST, t, v, traceback):
        try:
            if t is SystemExit or issubclass(t, Redirect):
                reraise(t, v, traceback)

            if issubclass(t, ConflictError):
                self.logConflicts(v, REQUEST)
                raise Retry(t, v, traceback)

            if t is Retry:
                try:
                    v.reraise()
                except:
                    # we catch the re-raised exception so that it gets
                    # stored in the error log and gets rendered with
                    # standard_error_message
                    t, v, traceback = sys.exc_info()
                if issubclass(t, ConflictError):
                    # ouch, a user saw this conflict error :-(
                    self.unresolved_conflict_errors += 1

            error_log_url = ''
            if not isinstance(published, list):
                try:
                    log = aq_acquire(published, '__error_log__', containment=1)
                except AttributeError:
                    pass
                else:
                    if log is not None:
                        error_log_url = log.raising((t, v, traceback))

            if (REQUEST is None or
                    (getattr(REQUEST.get('RESPONSE', None),
                             '_error_format', '') != 'text/html')):
                reraise(t, v, traceback)

            # Lookup a view for the exception and render it, then
            # raise the rendered value as the exception value
            # (basically the same that 'raise_standardErrorMessage'
            # does. The view is named 'index.html' because that's what
            # zope.publisher uses as well.
            view = queryMultiAdapter((v, REQUEST), name=u'index.html')
            if view is not None:
                if (IAcquirer.providedBy(view) and
                        IAcquirer.providedBy(published)):
                    view = view.__of__(published)
                else:
                    view.__parent__ = published
                v = view()
                if issubclass(t, Unauthorized):
                    # Re-raise Unauthorized to make sure it is handled
                    # correctly. We can't do that with all exceptions
                    # because some don't work with the rendered v as
                    # argument.
                    reraise(t, v, traceback)
                response = REQUEST.RESPONSE
                response.setStatus(t)
                response.setBody(v)
                return response

            if (published is None or published is app or
                    isinstance(published, list)):
                # At least get the top-level object
                published = app.__bobo_traverse__(REQUEST).__of__(
                    RequestContainer(REQUEST))

            published = getattr(published, 'im_self', published)
            while 1:
                f = getattr(published, self.raise_error_message, None)
                if f is None:
                    published = aq_parent(published)
                    if published is None:
                        reraise(t, v, traceback)
                else:
                    break

            client = published
            while 1:
                if getattr(client, self.error_message, None) is not None:
                    break
                client = aq_parent(client)
                # If we are going in circles without getting the error_message
                # let the response handle it
                if client is None or aq_base(client) is aq_base(published):
                    response = REQUEST.RESPONSE
                    response.exception()
                    return response

            if REQUEST.get('AUTHENTICATED_USER', None) is None:
                REQUEST['AUTHENTICATED_USER'] = AccessControl.User.nobody

            result = f(client, REQUEST, t, v, traceback,
                       error_log_url=error_log_url)
            if result is not None:
                t, v, traceback = result
                if issubclass(t, Unauthorized):
                    # Re-raise Unauthorized to make sure it is handled
                    # correctly. We can't do that with all exceptions
                    # because some don't work with the rendered v as
                    # argument.
                    reraise(t, v, traceback)
                response = REQUEST.RESPONSE
                response.setStatus(t)
                response.setBody(v)
                return response
        finally:
            traceback = None

EXCEPTION_HOOK = ExceptionHook()
