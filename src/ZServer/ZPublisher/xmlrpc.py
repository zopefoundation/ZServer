from zope.deferredimport import deprecatedFrom
deprecatedFrom(
    "Import from ZPublisher.xmlrpc instead",
    'ZPublisher.xmlrpc',
    'Response', 'is_xmlrpc_response', 'response',
    'dump_instance', 'parse_input', 'WRAPPERS',
)
