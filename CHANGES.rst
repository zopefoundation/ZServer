Changelog
=========

4.0b1 (2017-09-18)
------------------

- Update code to Zope 4.0b1.

4.0a2 (2017-01-20)
------------------

- Remove mechanize based testbrowser support.

- Use `@implementer` class decorator.

4.0a1 (2016-09-09)
------------------

- Broke out ZServer and related code from Zope core project.

  This includes FTP, webdav and xml-rpc handling, zope.conf support
  for ZServer related configuration and instance creation and zdaemon
  based startup logic.

  The mkzopeinstance, runzope, zopectl and zpasswd scripts are now
  provided by this project.

3.0 (2016-08-06)
----------------

- Create a separate distribution called `ZServer` without any code
  inside it. This allows projects to depend on this project for
  the Zope 2.13 release line.
