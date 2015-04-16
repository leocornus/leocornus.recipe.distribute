.. contents:: Table of Contents
   :depth: 5

Overview
========

This buildout_ recipe provides a easy way to manage multiple packages
with different types.

Options
=======

:source-root:
  The root directory where we find out the packages' source files.

:packages:
  A list of packages' name followed with verion number.

:dist-format:
  Available formats: zip, tar, gztar, bztar.
  Default format is ``zip``.

:output-root:
  The output root dir, where the archived file saved.  
  Default is parts directory.

Sample for distribute exact packages
====================================

Samples here are based on zc.buildout's testing support.
Check `testing support 
<http://pypi.python.org/pypi/zc.buildout/1.5.2#testing-support>`_ 
for more details.

Preparing Dirs and Files
------------------------

Some preparation.::

    >>> import os
    >>> srcRoot = tmpdir('src-root')
    >>> print(srcRoot)
    /.../src-root
    >>> distRoot = tmpdir('dist-root')
    >>> print(distRoot)
    /.../dist-root

preparting the test pakcages:
create some folders,
write some testing files too.::

    >>> packageOne = os.path.join(srcRoot, 'test-package-one')
    >>> mkdir(packageOne)
    >>> mkdir(os.path.join(packageOne, 'folderone'))
    >>> mkdir(os.path.join(packageOne, 'foldertwo'))
    >>> mkdir(os.path.join(packageOne, 'foldertwo', 'foldertwo2'))
    >>> write(packageOne, 'README.txt', "Readme content")
    >>> write(packageOne, 'folderone', 'fileone.txt', 'File one content')
    >>> write(packageOne, 'foldertwo', 'filetwo.txt', 'file two content')
    >>> write(packageOne, 'foldertwo', 'foldertwo2', 'filetwo2.txt', 'file two 2 content')
    >>> packagetwo = os.path.join(srcRoot, 'test-package-two')
    >>> mkdir(packagetwo)
    >>> mkdir(os.path.join(packagetwo, 'folder2one'))
    >>> mkdir(os.path.join(packagetwo, 'folder2two'))
    >>> mkdir(os.path.join(packagetwo, 'folder2two', 'folder2two2'))
    >>> write(packagetwo, 'README.txt', "Readme content")
    >>> write(packagetwo, 'folder2one', 'fileone.txt', 'File one content')
    >>> write(packagetwo, 'folder2two', 'folder2two2', 'filetwo2.txt', 'file two 2 content')

Create the buildout.cfg
-----------------------

The sample buildout config file.
The ``sample_buildout`` is the temp folder for testing.::

    >>> write(sample_buildout, 'buildout.cfg',
    ... """
    ... [buildout]
    ... parts = 
    ...     test-source-dist
    ...
    ... [test-source-dist]
    ... recipe = leocornus.recipe.distribute
    ... source-root = %(srcRoot)s
    ... packages = 
    ...     test-package-one=1.0
    ...     test-package-two=2.0
    ... dist-format = zip
    ... output-root = %(distRoot)s
    ... """ % dict(srcRoot=srcRoot, distRoot=distRoot))
    >>> ls(sample_buildout)
    d  bin
    -  buildout.cfg
    d  develop-eggs
    d  eggs
    d  parts

Execute and Verify
------------------

run the buildout::

    >>> os.chdir(sample_buildout)
    >>> print(system(buildout))
    Installing test-source-dist.
    test-source-dist: Found 2 packages in total!
    test-source-dist: Processing 1 of 2 packages - test-package-one
    test-source-dist: Creating package: .../dist-root/test-package-one.1.0.zip
    test-source-dist: Wiki Update: skip - Wiki update is OFF
    test-source-dist: Processing 2 of 2 packages - test-package-two
    test-source-dist: Creating package: .../dist-root/test-package-two.2.0.zip
    test-source-dist: Wiki Update: skip - Wiki update is OFF
    test-source-dist: Creating versions list file: .../dist-root/versions.txt...

Read the dist file to verify the result.::

    >>> import zipfile
    >>> thezip = zipfile.ZipFile(os.path.join(distRoot, 'test-package-one.1.0.zip'), "r")
    >>> files = thezip.namelist()
    >>> print(files)
    ['test-package-one/...']
    >>> len(files)
    4
    >>> 'test-package-one/README.txt' in files
    True
    >>> 'test-package-one/folderone/fileone.txt' in files
    True
    >>> 'test-package-one/foldertwo/filetwo.txt' in files
    True
    >>> 'test-package-one/foldertwo/foldertwo2/filetwo2.txt' in files
    True

verify package two::

    >>> thezip = zipfile.ZipFile(os.path.join(distRoot, 'test-package-two.2.0.zip'), "r")
    >>> files = thezip.namelist()
    >>> len(files)
    3
    >>> 'test-package-two/README.txt' in files
    True
    >>> 'test-package-two/folder2one/fileone.txt' in files
    True
    >>> 'test-package-two/folder2two/folder2two2/filetwo2.txt' in files
    True

verify the versions list file::

    >>> versions = open(os.path.join(distRoot, 'versions.txt'), 'r')
    >>> for line in versions:
    ...     print(line)
    test-package-one=1.0
    test-package-two=2.0

Sample to distribute whole folder
=================================

We will distirbue the whole WordPress plugins or themes folder.
Here a list of things we are going to do:

- preparing some testing folders and files to simulate WordPress
  Plugins and Themes
- create **buildout.cfg** with the distribute recipe to archive all
  plugins and themes
- verify the generated zip files have the correct content.

Prepare Plugins and Themes
--------------------------

We will use the same testing folders and files from previous example.

Make a WordPres Plugin package, could be any PHP file::

    >>> pluginData = """
    ... /**
    ...  * Plugin Name: Package One
    ...  * Plugin URI: http://www.pluginone.com
    ...  * Description: this the a dummy testing plugin.
    ...  * Version: 2.3.4
    ...  */
    ... ** Some other content.
    ... Testing the case for duplicate header patterns.
    ... Version: 4.5
    ... """
    >>> write(packageOne, 'pone.php', pluginData)

Make a WordPress Theme package, 
has to be the exact file name **style.css**::

    >>> themeData = """
    ... /**
    ...  * Theme Name: Package Two Theme.
    ...  * Theme URI: http://www.themeone.com
    ...  * Description: this is a dummy theme for testing.
    ...  * Version: 3.4.5
    ...  * other header content.
    ...  */
    ... ** other style contnet.
    ... Another duplicate header pattern.
    ... Theme Name: fake one.
    ... """
    >>> write(packagetwo, 'style.css', themeData)

Create the buildout file
------------------------

The buildout will be very simple::

    >>> write(sample_buildout, 'buildout.cfg',
    ... """
    ... [buildout]
    ... parts =
    ...     test-source-dist
    ...
    ... [test-source-dist]
    ... recipe = leocornus.recipe.distribute
    ... source-root = %(srcRoot)s
    ... packages = ALL
    ... dist-format = zip
    ... output-root = %(distRoot)s
    ... """ % dict(srcRoot=srcRoot, distRoot=distRoot))
    >>> ls(sample_buildout)
    -  .installed.cfg
    d  bin
    -  buildout.cfg
    d  develop-eggs
    d  eggs
    d  parts

Execute and Verify
------------------

Execute the buildout::

    >>> os.chdir(sample_buildout)
    >>> print(system(buildout))
    Uninstalling test-source-dist.
    Installing test-source-dist.
    test-source-dist: Found 2 packages in total!
    test-source-dist: Processing 1 of 2 packages - test-package-one
    test-source-dist: Creating package: .../test-package-one.2.3.4.zip
    test-source-dist: Wiki Update: skip - Wiki update is OFF
    test-source-dist: Processing 2 of 2 packages - test-package-two
    test-source-dist: Creating package: .../test-package-two.3.4.5.zip
    test-source-dist: Wiki Update: skip - Wiki update is OFF
    ...

Read the zip file and verify the content.
We will expect the following files are created::

    >>> pOne = os.path.join(distRoot, 'test-package-one.2.3.4.zip')
    >>> os.path.exists(pOne)
    True
    >>> tTwo = os.path.join(distRoot, 'test-package-two.3.4.5.zip')
    >>> os.path.exists(tTwo)
    True

.. _buildout: https://github.com/buildout/buildout
