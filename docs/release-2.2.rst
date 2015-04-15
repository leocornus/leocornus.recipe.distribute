
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

The wiki resource file should have all details information
aobut the wiki template and extrction patterns.

Sample of .mwrc file
--------------------

Here is a sample .mwrc file::

  [mwclient]
  host = domain.name.com
  path = /wiki/
  username = seanchen
  password = mypassword

  [template fields]
  internet_page: [%(package_uri)s plugin homepage]
  download: [http://www.bases.com/repos/%(package_name)s.%(latest_version)s.zip %(package_name)s.%(latest_version)s.zip]

  [template]
  wiki_template: {{Feature Infobox
    |name=%(name)s
    |internet_page=%(internet_page)s
    |description=%(description)s
    |latest_version=%(latest_version)s
    |download=%(download)s}}

  [headers]
  latest_version: Version:.*
  name: (Plugin|Theme) Name:.*
  description: Description:.*
  package_uri: (Plugin|Theme) URI:.*
  author: Author:.*
  author_uri: Author URI:.*
  
  [headers default]
  latest_version: 1.0

Process flow
------------

Steps to process each package:

#. Extract file headers from a file, the **header** section
   will define the pattern for each file header and 
   assign a field name for it.
   The **header default** section will provide default value for
   each file header.
   If no default value set, we will use empty string 
   as default value.
#. Prepare the values for wiki template.
   The section **template fields** defines the template fields,
   which need process before fill in the template.

Questions
---------

- Should we allow user to set credentials to wiki site?

Playground for mwclient
-----------------------

Using mwclient_ to communicate with MediaWiki site.
Check Python sandbox `mwclient story`_ for how to use mwclient_.

.. _mwclient: https://github.com/btongminh/mwclient
.. _mwclient story: https://github.com/leocornus/leocornus.py.sandbox/blob/master/leocornus/py/sandbox/tests/mwclient
