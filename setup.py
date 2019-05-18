##############################################################################
#
# Copyright (c) 2010 Zope Foundation and Contributors.
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

from setuptools import setup, find_packages

version = '4.0.1'

setup(
    name='ZServer',
    version=version,
    url='https://github.com/zopefoundation/ZServer',
    license='ZPL 2.1',
    description="Zope ZServer.",
    author='Zope Foundation and Contributors',
    author_email='zope-dev@zope.org',
    long_description=(open('README.rst').read() + '\n' +
                      open('CHANGES.rst').read()),
    packages=find_packages('src'),
    package_dir={'': 'src'},
    classifiers=[
        "Development Status :: 6 - Mature",
        "Environment :: Web Environment",
        "Framework :: Zope",
        "Framework :: Zope :: 4",
        "License :: OSI Approved :: Zope Public License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2 :: Only",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    install_requires=[
        'setuptools',
        'AccessControl',
        'Acquisition',
        'ExtensionClass',
        'Persistence',
        'transaction',
        'ZConfig',
        'zdaemon',
        'zExceptions',
        'ZODB',
        'zope.component',
        'zope.container',
        'zope.contenttype',
        'zope.deferredimport',
        'zope.event',
        'zope.interface',
        'zope.lifecycleevent',
        'zope.processlifetime',
        'zope.schema',
        'zope.testing',
        'Zope >= 4.0b6',
    ],
    extras_require={
        'sdnotify': ['sdnotify'],
    },
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            ('mkzopeinstance='
                'ZServer.Zope2.utilities.mkzopeinstance:main'),
            'runzope=ZServer.Zope2.Startup.run:run',
            'zopectl=ZServer.Zope2.Startup.zopectl:run',
            'zpasswd=ZServer.Zope2.utilities.zpasswd:main',
        ],
    },
)
