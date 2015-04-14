
Release 2.2
===========

- Ability to save the summary of all packages as MediaWiki page.

MediaWiki Dependence
--------------------

This new feature will depend on a live MediaWiki site.
And we will assume there is a wiki template definded
a set of fields to store those package information.

check `sandbox story <https://github.com/leocornus/leocornus.py.sandbox/blob/master/leocornus/py/sandbox/tests/mwclient/wpFileHeader2mw.rst>`_ for more details.

New recipe options
------------------

design new options for this recipe.

:update-wiki:
  switch to turn on or off wiki connection. default is **off**.
:wiki-rc-file:
  the full path to the .mwrc file. default is **~/.mwrc**.
:wiki-template-name:
  the name for the wiki template, default is **Feature Infobox**.
:wiki-template-download-base:
  the base URL to download this package.

Questions
~~~~~~~~~

- Should we allow user to set credentials to wiki site?

Playground for mwclient
-----------------------

Using mwclient_ to communicate with MediaWiki site.
Check Python sandbox `mwclient story`_ for how to use mwclient_.

.. _mwclient: https://github.com/btongminh/mwclient
.. _mwclient story: https://github.com/leocornus/leocornus.py.sandbox/blob/master/leocornus/py/sandbox/tests/mwclient
