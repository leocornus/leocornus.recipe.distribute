
Overview
========

This is for testing the basic usage for Fabric's local operator.
The local operator is used to run commands on local machine.

    >>> from fabric.operations import local
    >>> from fabric.context_managers import lcd
    >>> import os

Very basic things.
The with context was introduced since Python 2.7

    >>> with lcd('/usr'):
    ...     local('pwd', True)
    ...     local('ls -la', False)
    ...     local('pwd', False)
    [localhost] local: pwd
    '/usr'
    [localhost] local: ls -la
    ''
    [localhost] local: pwd
    ''

Testing copy files.
