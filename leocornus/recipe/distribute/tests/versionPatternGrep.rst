This is a playground to try out Python regular expressions module.
This is mainly covered by the following topics:

* https://docs.python.org/2/library/re.html
* https://docs.python.org/2/tutorial/inputoutput.html

TODO
----

- search file name pattern in a folder to get a list of files
- search pattern in file content to get the version number

import modules
--------------

We will using the following modules:

    >>> import os
    >>> import shutil
    >>> import re
    >>> import fnmatch

Preparing folders and files
---------------------------

We will using the home folder for testing.

    >>> homeFolder = os.path.expanduser('~')

Create folders.

    >>> testFolder = os.path.join(homeFolder, 'testFolder')
    >>> folderOne = os.path.join(testFolder, 'folderOne')
    >>> folderTwo = os.path.join(testFolder, 'folderTwo')
    >>> os.mkdir(testFolder)
    >>> os.mkdir(folderOne)
    >>> os.mkdir(folderTwo)
    >>> os.path.isdir(testFolder)
    True
    >>> os.path.isdir(folderOne)
    True
    >>> os.path.isdir(folderTwo)
    True

open file to write. the mode **r+** is for both read and write
a file.

    >>> fileOne = os.path.join(folderOne, 'fileone.txt')
    >>> fileTwo = os.path.join(folderTwo, 'filetwo.txt')
    >>> os.system("touch " + fileOne)
    0
    >>> os.system("touch " + fileTwo)
    0
    >>> f = open(fileOne, 'r+')
    >>> f.write("This is a test.\n")
    >>> f.write(
    ... """This line count too
    ... line two
    ... This is line three
    ... """)
    >>> f.close()
    >>> f = open(fileOne, 'r')
    >>> f.readline()
    'This is a test.\n'
    >>> f.readline()
    'This line count too\n'
    >>> f.readline()
    'line two\n'
    >>> f.readline()
    'This is line three\n'
    >>> f.close()

Try to search the file name filename pattern

    >>> for file in os.listdir(testFolder):
    ...     print file
    ...     if fnmatch.fnmatch(file, '.txt'):
    ...         print file
    'folderOne'
    'folderTwo'

Testing os.walk method.
It is very useful. we need have an option called **depth**,
which will set how deep of the subdirectory.

    >>> for root, dirs, files in os.walk(testFolder):
    ...     print 'root: ' + root
    ...     print dirs
    ...     print files

Questions
---------

- how to search files by file name pattern in a folder?
- how to search file content to find a pattern?

Read File and Search
--------------------

Create a file for read and search...

Clean up
--------

remove the whole test folder.

    >>> shutil.rmtree(testFolder)