This is playground to try out how Python modules for 
Data Compression and Archiving. 
This is mainly covered by the following 2 topic:

 * http://docs.python.org/library/archiving.html
 * http://docs.python.org/library/shutil.html#archiving-operations

Handling Zip File
=================

Create zip file from a folder.
Testing adding files to a zip file.
Ignore files match certain patterns.

    >>> import os
    >>> import zipfile
    >>> import shutil

Using the home folder for testing.

    >>> homeFolder = os.path.expanduser('~')

Preparing some testing files.

    >>> testFolder = os.path.join(homeFolder, 'testfolder')
    >>> os.mkdir(testFolder)
    >>> os.mkdir(os.path.join(testFolder, 'folderone'))
    >>> os.mkdir(os.path.join(testFolder, 'foldertwo'))
    >>> os.system("touch " + os.path.join(testFolder, 'folderone', 'one'))
    0
    >>> os.system("touch " + os.path.join(testFolder, 'foldertwo', 'two'))
    0

Get ready the ZipFile object.

    >>> zip_filename = os.path.expanduser(os.path.join("~", 'mytest.zip'))
    >>> zip = zipfile.ZipFile(zip_filename, "w", 
    ...     compression=zipfile.ZIP_DEFLATED)

Using os.chdir to the root dir, then using os.walk to get all files.

    >>> os.chdir(homeFolder)
    >>> for dirpath, dirnames, filenames in os.walk('./testfolder'):
    ...     for name in filenames:
    ...         path = os.path.normpath(os.path.join(dirpath, name))
    ...         if os.path.isfile(path):
    ...             zip.write(path, path)
    >>> zip.close()

How to verify the result.
namelist will list the file names in the zip file.
Not sure about the order, might be random.
So using different way to verify.

    >>> files = zip.namelist()
    >>> len(files)
    2
    >>> 'testfolder/folderone/one' in files
    True
    >>> 'testfolder/foldertwo/two' in files
    True

now some clean up...
os.rmdir can ONLY remove empty folder.
shutil.rmtree offers a convenient way to remove the whole folder, 
even it is NOT an empty folder.  
This method was added since Python 2.6

    >>> shutil.rmtree(testFolder)
    >>> os.remove(os.path.join(homeFolder, 'mytest.zip'))

A peak on shutil module
=======================

Since Python version 2.7, make_archive is the one stop 
shop for making archive files by using Python.

    >>> archive_name = os.path.expanduser(os.path.join('~', 'test'))
    >>> zip_name = shutil.make_archive(archive_name, 'zip', '/var/tmp')
    >>> zip_name == archive_name + ".zip"
    True

Now check to see if the zip file are created.

    >>> home_folder_files = os.listdir(os.path.expanduser('~'))
    >>> 'test.zip' in home_folder_files
    True
