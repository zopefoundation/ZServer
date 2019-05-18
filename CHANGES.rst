Changelog
=========

4.0.1 (2019-05-17)
------------------

- Fixed configuration file path in tests


4.0 (2019-05-08)
----------------

Changes since 3.0:

- Broke out ZServer and related code from Zope core project.

  This includes FTP, webdav and zope.conf support
  for ZServer related configuration and instance creation and zdaemon
  based startup logic.

  The mkzopeinstance, runzope, zopectl and zpasswd scripts are now
  provided by this project.

- The ``enable-product-installation`` `zope.conf` setting is now a no-op.

- Changed `zope.conf` default settings for ``zserver-threads`` to ``2``.

- Add optional support for systemd sd_notify().

- Remove mechanize based testbrowser support.

- Use `@implementer` class decorator.


3.0 (2016-08-06)
----------------

- Create a separate distribution called `ZServer` without any code
  inside it. This allows projects to depend on this project for
  the Zope 2.13 release line.
