
# __init__.py

import logging
import os
import zipfile

class Dist:
    """The main class.
    """

    # buildout recipe's constructor,
    # buildout will use this to create a recipe instance.
    def __init__(self, buildout, name, options):

        self.options = options
        # part's name.
        self.name = name
        self.buildout = buildout

        options.setdefault('dist-format', 'zip')
        options.setdefault('output-root', 
            buildout['buildout']['parts-directory'])

        # get the packages options.
        pkgs = options.get('packages', '').strip()
        if pkgs == 'ALL':
            self.packages = ''
        else:
            pkgs = pkgs.splitlines()
            # the packages will have name, version format.
            self.packages = [package.strip().split('=') 
                             for package in pkgs if package.strip()]

    # install method.
    def install(self):

        log = logging.getLogger(self.name)
        if self.packages == '':
            log.info('No Package Specified!')
            return []

        sourceRoot = self.options.get('source-root')
        outputRoot = self.options.get('output-root')
        format = self.options.get('dist-format')

        #  TODO: only support zip format for now.

        return self.zipdist(sourceRoot, outputRoot, self.packages)

    # update method.
    def update(self):

        pass

    # make zip distribute
    def zipdist(self, srcRoot, distRoot, packages):

        log = logging.getLogger(self.name)
        # return the installed parts.
        parts = []

        # work on the srouce root dir.
        os.chdir(srcRoot)
        for package, version in packages:
            # preparing the zip file name
            zipFilename = package + "." + version + ".zip"
            # we need the full path.
            zipFilename = os.path.join(distRoot, zipFilename)
            log.info('Creating package: %s' % zipFilename)

            zip = zipfile.ZipFile(zipFilename, "w",
                compression = zipfile.ZIP_DEFLATED)
            for dirpath, dirnames, filenames in os.walk('./' + package):
                for name in filenames:
                    path = os.path.normpath(os.path.join(dirpath, name))
                    if os.path.isfile(path):
                        zip.write(path, path)
            # close to write to disk.
            zip.close()
            parts.append(zipFilename)

        return parts
