
Overview
========

Let's get start.

    >>> print 'Hello'
    Hello

Options
=======

``source-root``

    The root directory where we find out the packages' source files.

``packages``

    A list of packages' name followed with verion number.

``dist-format``

    Available formats: zip, tar, gztar, bztar.
    Default format is ``zip``.

``output-root``

    The output root dir, where the archived file saved.  
    Default is parts directory.

Samples
=======

Samples here are based on zc.buildout's testing support.
Check http://pypi.python.org/pypi/zc.buildout/1.5.2#testing-support for more
details.

Some preparation.

    >>> import os
    >>> srcRoot = tmpdir('src-root')
    >>> distRoot = tmpdir('dist-root')

preparting the test pakcages:
create some folders,
write some testing files too.

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
    ... source-root = %(srcRoot)s
    ... packages = 
    ...     test-package-one=1.0
    ...     test-package-two=2.0
    ... dist-format = zip
    ... output-root = %(distRoot)s
    ... """ % dict(srcRoot=srcRoot, distRoot=distRoot))

run the buildout

    >>> print system(buildout)
    Installing test-source-dist.
    test-source-dist: Creating package: .../dist-root/test-package-one.1.0.zip
    test-source-dist: Creating package: .../dist-root/test-package-two.2.0.zip

Read the dist file to verify the result.

    >>> import zipfile
    >>> thezip = zipfile.ZipFile(os.path.join(distRoot, 'test-package-one.1.0.zip'), "r")
    >>> files = thezip.namelist()
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

Package two

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
