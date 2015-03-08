
# __init__.py

import logging
import os
import zipfile
import subprocess

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
            # query the whole source folder for certain patterns.
            # and then get ready the package list.
            sourceRoot = self.options.get('source-root')
            self.packages = self.wpPackages(sourceRoot)
        else:
            pkgs = pkgs.splitlines()
            # the packages will have name, version format.
            # here is an example::
            #
            #   packages = [
            #     [nameone, versionone],
            #     [nametwo, versiontwo]
            #   ]
            self.packages = [package.strip().split('=') 
                             for package in pkgs if package.strip()]

    # install method.
    def install(self):

        log = logging.getLogger(self.name)
        if self.packages == '':
            # return without do anything.
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

    # query source folder to find WordPress Plugins or Themes.
    def wpPackages(self, srcRoot):

        # using grep the query files in the source folder.
        # the plugin grep query pattern.
        pluginPattern = "grep -l 'Plugin Name: ' " + \
                        srcRoot + "/*/*.php"
        plugins = subprocess.check_output(pluginPattern, shell=True)
        # the theme grep query pattern.
        themePattern = "grep -l 'Theme Name: ' " + \
                       srcRoot + "/*/style.css"
        themes = subprocess.check_output(themePattern, shell=True)
        packages = plugins + themes
        pkgs = []
        for package in packages.strip().splitlines():
            dirName = os.path.dirname(package)
            # package name
            pkgName = os.path.basename(dirName)
            # version grep pattern.
            versionPattern = "grep -oE 'Version: .*' " \
                             + package.decode('ascii')
            version = subprocess.check_output(versionPattern,
                                              shell=True)
            # clean up 
            version = version.strip().split(":")
            pkgVersion = version[1].strip()
            pkgs.append([pkgName, pkgVersion])

        return pkgs

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
