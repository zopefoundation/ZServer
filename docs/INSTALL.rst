Installing ZServer with ``zc.buildout``
=======================================

.. highlight:: bash

This document describes how to get going with a ZServer based Zope
using ``zc.buildout``.


About ``zc.buildout``
---------------------

`zc.buildout <https://pypi.python.org/pypi/zc.buildout>`_ is a powerful
tool for creating repeatable builds of a given software configuration
and environment.  The Zope developers use ``zc.buildout`` to develop
Zope itself, as well as the underlying packages it uses.

Prerequisites
-------------

In order to use Zope with ZServer, you must have the following
pre-requisite available:

- A supported version of Python, including the development support if
  installed from system-level packages. Supported versions include:

  * 2.7.x

- Zope needs the Python ``zlib`` module to be importable.  If you are
  building your own Python from source, please be sure that you have the
  headers installed which correspond to your system's ``zlib``.

- A C compiler capable of building extension modules for your Python
  (gcc recommended).


Installing ZServer using zc.buildout
------------------------------------

In this configuration, we use ``zc.buildout`` to install the Zope software,
and then generate a server "instance" inside the buildout environment.

Installing the ZServer software
:::::::::::::::::::::::::::::::

Installing the ZServer software using ``zc.buildout`` involves the
following steps:

- Download the ZServer source distribution from `PyPI`__

  __ https://pypi.python.org/pypi/ZServer

- Bootstrap the buildout

- Run the buildout

On Linux, this can be done as follows::

  $ wget https://pypi.python.org/packages/source/Z/ZServer/ZServer-<version>.tar.gz
  $ tar xfvz ZServer-<version>.tar.gz
  $ cd ZServer-<version>
  $ /path/to/your/python bootstrap.py
  $ bin/buildout


Creating a ZServer instance
:::::::::::::::::::::::::::

Once you've installed ZServer, you will need to create an "instance
home". This is a directory that contains configuration and data for a
ZServer process.  The instance home is created using the
``mkzopeinstance`` script::

  $ bin/mkzopeinstance -d .

You will be asked to provide a user name and password for an
administrator's account during ``mkzopeinstance``. To see the available
command-line options, run the script with the ``--help`` option::

  $ bin/mkzopeinstance --help


Running ZServer
:::::::::::::::

After you installed the ZServer instance, you can start it via:

  $ bin/runzope -C etc/zope.conf -X "debug-mode=on"

Leave out the "debug-mode=on" option for production use.

If you prefer to use zopectl, you can run it via:

  $ bin/zopectl -C etc/zope.conf -p bin/runzope fg
