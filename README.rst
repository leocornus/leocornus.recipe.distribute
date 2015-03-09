leocornus.recipe.distribute
===========================

A buildout recipe to package and distribute lib, module, archive, files, etc.

Travis Build Status: |travis|

A simple buildout part to archive all skins in wiki skin folder::

  [archive-skins]
  recipe = leocornus.recipe.distribute
  source-root = /full/path/to/wiki/skins
  packages = ALL
  dist-format = zip
  output-root = /full/path/to/archive/folder

The **packages = ALL** tells the distribute recipe to archive all
folders in the source-root folder.

More details in 
`package README.rst <leocornus/recipe/distribute/README.rst>`_

Change Logs
-----------

Release 2.0.0

- Ability to distribute all WordPress plugins and themes under
  a folder.

License
-------

`GPL license <LICENSE.GPL>`_

.. |travis| image:: https://api.travis-ci.org/leocornus/leocornus.recipe.distribute.png
