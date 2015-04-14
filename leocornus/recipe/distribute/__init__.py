
# __init__.py

import logging
import os
import zipfile
import subprocess
from leocornus.recipe.distribute.utils import extract_wp_header

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
            self.packages = []
            for package in pkgs:
                if package.strip():
                    name, version = package.strip().split('=')
                    header = {"Version" : version}
                    self.packages.append([name, header])

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
        pluginP = "grep -l 'Plugin Name: ' %s/*/*.php" % srcRoot
        try:
            plugins = subprocess.check_output(pluginP, shell=True)
        except subprocess.CalledProcessError:
            # logging no plugin found.
            plugins = ""

        # the theme grep query pattern.
        themeP = "grep -l 'Theme Name: ' %s/*/style.css" % srcRoot
        try:
            themes = subprocess.check_output(themeP, shell=True)
        except subprocess.CalledProcessError:
            # logging not theme found.
            themes = ""

        packages = plugins + themes
        pkgs = []
        for package in packages.strip().splitlines():
            dirName = os.path.dirname(package)
            # package name
            pkgName = os.path.basename(dirName)
            # Version pattern is not found, give
            # default version 1.0
            header = extract_wp_header(package.decode('ascii'), 
                                       Version='1.0')
            # logging the message...
            pkgs.append([pkgName, header])

        return pkgs

    # make zip distribute
    def zipdist(self, srcRoot, distRoot, packages):

        log = logging.getLogger(self.name)
        # return the installed parts.
        parts = []
        # get ready the version list file, the content
        # packageone=versone
        # packagetwo=versiontwo
        versionsList = os.path.join(distRoot, 'versions.txt')
        versions = open(versionsList, 'w')

        # work on the srouce root dir.
        os.chdir(srcRoot)
        for package, header in packages:
            version = header['Version']
            # write to versions list
            versions.write("""%s=%s\n""" % (package, version))
            # preparing the zip file name
            zipFilename = package + b"." + version + b".zip"
            # we need the full path.
            zipFilename = os.path.join(distRoot, zipFilename)
            log.info('Creating package: %s' % zipFilename)

            zip = zipfile.ZipFile(zipFilename, "w",
                compression = zipfile.ZIP_DEFLATED)
            for dirpath, dirnames, filenames in os.walk(b'./' + package):
                for name in filenames:
                    path = os.path.normpath(os.path.join(dirpath, name))
                    if os.path.isfile(path):
                        zip.write(path, path)
            # close to write to disk.
            zip.close()
            parts.append(zipFilename)

        # save the versions list file.
        log.info('Creating versions list file: %s' % versionsList)
        versions.close()

        return parts
