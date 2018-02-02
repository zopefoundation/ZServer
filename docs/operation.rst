Configuring and Running ZServer
===============================

.. highlight:: bash


Whichever method you used to install ZServer and create a server
instance (see :doc:`INSTALL`), the end result is configured and
operated the same way.


Configuring ZServer
-------------------

Your instance's configuration is defined in its ``etc/zope.conf`` file.
Unless you created the file manually, that file should contain a minimal
sample configuration. A fully annotated version should be available in
``etc/example.conf``.

When starting ZServer, if you see errors indicating that an address is in
use, then you may have to change the ports ZServer uses for HTTP or FTP.
The default HTTP and FTP ports used by ZServer are
8080 and 8021 respectively. You can change the ports used by
editing ./etc/zope.conf appropriately.

The section in the configuration file looks like this::

  <http-server>
    # valid keys are "address" and "force-connection-close"
    address 8080
    # force-connection-close on
  </http-server>

The address can just be a port number as shown, or a host:port
pair to bind only to a specific interface.

After making any changes to the configuration file, you need to restart any
running ZServer for the affected instance before changes are in effect.

Additionally if you've installed ZServer with the sdnotify extra and you are
on a Linux distribution using systemd, ZServer will tell your service it is
ready and also tell it to reset its watchdog timer every 30 seconds.

A sample service file::

    [Unit]
    Description=A test ZServer service

    [Service]
    # Note: setting PYTHONUNBUFFERED is necessary to see the output of this
    # service in the journal
    # See https://docs.python.org/2/using/cmdline.html#envvar-PYTHONUNBUFFERED
    Environment=PYTHONUNBUFFERED=true

    # Adjust this line to the correct path and params for your Zope instance
    ExecStart=/path/to/bin/runzope

    # Note that we use Type=notify here since ZServer will send "READY=1"
    # when it's finished starting up
    Type=notify

    # We'll assume it needs to get back to us at least every 45s or it is dead
    WatchdogSec=45

    # We'll always kick it back up if it is in a failure state
    # There are other values for this, including on-watchdog, read systemd docs
    Restart=always

Running ZServer in the Foreground
---------------------------------

To run ZServer without detaching from the console, use the ``runzope``
command::

  $ bin/runzope -C etc/zope.conf

In this mode, ZServer emits its log messages to the console, and does not
detach from the terminal.


Logging In To Zope
------------------

Once you've started ZServer, you can then connect to the Zope instance
by directing your browser to::

  http://yourhost:8080/manage

where 'yourhost' is the DNS name or IP address of the machine
running ZServer. If you changed the HTTP port as described, use the port
you configured.

You will be prompted for a user name and password. Use the user name
and password you provided in response to the prompts issued during
the "make instance" process.

Now you're off and running! You should be looking at the Zope
management screen which is divided into two frames. On the left you
can navigate between Zope objects and on the right you can edit them
by selecting different management functions with the tabs at the top
of the frame.

If you haven't used Zope before, you should head to the Zope web
site and read some documentation. The Zope Documentation section is
a good place to start. You can access it at https://zope.readthedocs.io/


Troubleshooting
---------------

- This version of ZServer requires Python 2.7 or better.
  It will *not* run with Python 3.x.

- To build Python extensions you need to have Python configuration
  information available. If your Python comes from an RPM you may
  need the python-devel (or python-dev) package installed too. If
  you built Python from source all the configuration information
  should already be available.
