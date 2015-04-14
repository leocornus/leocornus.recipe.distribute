|travis|_ |pypi-version|_ |pypi-download|_ |pypi-license|_ 
|gitter-img|_

leocornus.recipe.distribute
===========================

A buildout recipe to package and distribute lib, module, archive, files, etc.

A simple buildout part to archive all skins in wiki skin folder::

  [archive-skins]
  recipe = leocornus.recipe.distribute
  source-root = /full/path/to/wiki/skins
  packages = ALL
  dist-format = zip
  output-root = /full/path/to/archive/folder

The **packages = ALL** tells the distribute recipe to archive all
folders in the source-root folder.
A versions list text file (versions.txt) will be generated to 
list all packages in the following fomat::

  packageone=1.0
  packagetwo=2.0

More details in 
`package README.rst <leocornus/recipe/distribute>`_

Change Logs
-----------

- `Release 2.2.0 <docs/release-2.2.rst>`_

License
-------

`GPLv2 license <LICENSE.GPL>`_

.. |travis| image:: https://api.travis-ci.org/leocornus/leocornus.recipe.distribute.png
.. _travis: https://travis-ci.org/leocornus/leocornus.recipe.distribute
.. |pypi-version| image:: http://img.shields.io/pypi/v/leocornus.recipe.distribute.svg
.. _pypi-version: https://pypi.python.org/pypi/leocornus.recipe.distribute
.. |pypi-download| image:: http://img.shields.io/pypi/dm/leocornus.recipe.distribute.svg
.. _pypi-download: https://pypi.python.org/pypi/leocornus.recipe.distribute
.. |pypi-license| image:: http://img.shields.io/pypi/l/leocornus.recipe.distribute.svg
.. _pypi-license: https://pypi.python.org/pypi/leocornus.recipe.distribute
.. |gitter-img| image:: https://badges.gitter.im/Join%20Chat.svg
   :alt: Join the chat at https://gitter.im/leocornus/leocornus.recipe.distribute
.. _gitter-img: https://gitter.im/leocornus/leocornus.recipe.distribute?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
