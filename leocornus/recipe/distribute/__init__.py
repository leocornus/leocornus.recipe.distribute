
# __init__.py

import logging
import os
import zipfile
import subprocess
from leocornus.recipe.distribute.utils import MwrcSite

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
        options.setdefault('wiki-rc-file', '~/.mwrc')

        # get the wiki resource file:
        mwrc = options.get('wiki-rc-file').strip()
        self.wiki_site = MwrcSite(mwrc)

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
                    header = {"latest_version" : version}
                    self.packages.append([name, header])

    # install method.
    def install(self):

        log = logging.getLogger(self.name)
        if self.packages == '':
            # return without do anything.
            log.info('No Package Specified!')
            return []
        # log totale number of packages:
        log.info("Found %s packages in total!" % len(self.packages))

        sourceRoot = self.options.get('source-root')
        outputRoot = self.options.get('output-root')

        #  TODO: only support zip format for now.
        format = self.options.get('dist-format')

        return self.zipdist(sourceRoot, outputRoot, self.packages)

    # update method.
    def update(self):

        pass

    # query source folder to find WordPress Plugins or Themes.
    def wpPackages(self, srcRoot):

        log = logging.getLogger(self.name)
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
            headers = self.wiki_site.template_values(
                package.decode('ascii'), pkgName)
            pkgs.append([pkgName, headers])

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

        # work on the srouce root dir, so we could have the 
        # correct path for each package.
        os.chdir(srcRoot)
        index = 0
        total = len(packages)
        for package, header in packages:
            index = index + 1
            # Logging the progress...
            log.info('Processing %s of %s packages - %s' % 
                     (index, total, package))
            version = header['latest_version']
            # write to versions list
            versions.write("""%s=%s\n""" % (package, version))
            # preparing the zip file name
            zipFilename = "%s.%s.zip" % (package, version)
            # we need the full path.
            zipFilename = os.path.join(distRoot, zipFilename)
            log.info('Creating package: %s' % zipFilename)

            zip = zipfile.ZipFile(zipFilename, "w",
                compression = zipfile.ZIP_DEFLATED)
            # current folder is srcRoot
            for dirpath, dirnames, filenames in os.walk(package):
                for name in filenames:
                    # remove redundant separators and 
                    # up-level references
                    path = os.path.join(dirpath, name)
                    path = os.path.normpath(path)
                    zip.write(path)
            # close to write to disk.
            zip.close()
            parts.append(zipFilename)

            # call update_wiki method, the return value should
            # provide the status: create new, update, or error!
            ret = self.wiki_site.update_wiki(header)
            # logging the status message...
            log.info('Wiki Update: %(status)s - %(message)s' % ret)

        # save the versions list file.
        log.info('Creating versions list file: %s' % versionsList)
        versions.close()

        return parts
