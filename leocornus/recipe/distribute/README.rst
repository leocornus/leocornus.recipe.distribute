
Overview
========

Let's get start.

    >>> print 'Hello'
    Hello

Options
=======

``source-root-dir``

``version``

``version-file``

``dist-format``

    Available formats: zip, tar, gztar, bztar

``output-root-dir``

Samples
=======

Samples here are based on zc.buildout's testing support.
Check http://pypi.python.org/pypi/zc.buildout/1.5.2#testing-support for more
details.

Some preparation.

The sample buildout config file.
The ``sample_buildout`` is the temp folder for testing.

    >>> write(sample_buildout, 'buildout.cfg',
    ... """
    ... [buildout]
    ... parts = 
    ...     test-source-dist
    ...
    ... [test-source-dist]
    ... recipe = leocornus.recipe.distribute
    ... source-root-dir = %(src-root)
    ... packages = 
    ... version = 1.0
    ... dist-format = zip
    ... output-root-dir = %(dist-root)
    ... """ % dict(src-root=src-root, dist-root=dist-root))
