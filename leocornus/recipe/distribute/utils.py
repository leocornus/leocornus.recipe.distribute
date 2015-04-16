# utils.py

# save some utility functions here.

import os
import subprocess
import mwclient

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

def extractHeader(pattern, fullFilePath, default):
    """extract header field values from the given file.
    """
    grepPattern = """grep -oE '%s' %s""" % (pattern, fullFilePath)
    try:
        ret = subprocess.check_output(grepPattern, shell=True)
        # only split the first ":"!
        # this will avoid the confuse with the ":" in an URI.
        ret = ret.strip().split(b":", 1)
        return ret[1].strip()
    except subprocess.CalledProcessError:
        # could not find the pattern, return default value?
        return default


def extract_wp_header(filepath, **default):
    """extract WordPress file header fields values in a dict.

    filepath should be the full path to the file.
    default will provide the available default value.
    We will support the following file header field:

    - Plugin|Theme Name as Name
    - Plugin|Theme URI as URI
    - Description
    - Version
    - Author
    - Author URI
    """

    # preparing the patterns.
    patterns = ['Version:.*',
                '(Plugin|Theme) Name:.*',
                'Description:.*',
                '(Plugin|Theme) URI:.*',
                'Author:.*',
                'Author URI:.*'
               ]

    # return as a dict.
    ret = {}
    for pattern in patterns:
        # get the field name:
        field_name = pattern.split(b":")[0]
        # the grep pattern.
        grep_pattern = """grep -oE '%s' %s""" % (pattern, filepath)

        try:
            value = subprocess.check_output(grep_pattern, shell=True)
            # only split the first ":"
            value = value.strip().split(b":", 1)
            ret[field_name] = value[1].strip()
        except subprocess.CalledProcessError:
            # could NOT find the pattern.
            if default.has_key(field_name):
                ret[field_name] = default[field_name]
            else:
                ret[field_name] = ""

    return ret

# my MediaWiki site.
class MwrcSite(object):
    """The MediaWiki site reading site info from a resouce file.

    The default resource file is located at ~/.mwrc.
    """

    def __init__(self, rcfile=None):
        """Construct a site from the given resource file.
        """

        self.rcfile = rcfile
        if rcfile == None:
            # will try the default resource file location:
            # ~/.mwrc
            homeFolder = os.path.expanduser("~")
            self.rcfile = os.path.join(homeFolder, '.mwrc')

        self.site = None
        self.headers_info = None
        self.headers_default = None
        self.template_info = None
        self.template_fields = []

        # try to read the rcfile and create a site instance.
        if os.path.exists(self.rcfile):
            # read wiki site information from the resource file.
            rc = configparser.ConfigParser()
            filename = rc.read(self.rcfile)
            self.headers_info = rc.items('headers')
            self.headers_default = dict(rc.items('headers default'))
            self.templates = dict(rc.items('template', True))
            self.template_fields = rc.items('template fields', True)
            mwinfo = dict(rc.items('mwclient'))
            # TODO: need check if those values are set properly!
            if mwinfo.has_key('host'):
                self.site = mwclient.Site(mwinfo['host'], 
                                          path=mwinfo['path'])
                self.site.login(mwinfo['username'], 
                                mwinfo['password'])
        else:
            # need set up the default values for header info.
            # only need version.
            self.headers_info = [('latest_version', 'Version:.*')]

    def page_exists(self, title):
        """return true if a wiki page with the same title exists
        """

        if self.site == None:
            return False
        else:
            thepage = self.site.Pages[title]
            return thepage.exists

    def create_page(self, title, content, comment):
        """Create a new page with the given title, 
        content and comment
        """

        ret = None
        if self.site == None:
            ret = None
        else:
            thepage = self.site.Pages[title]
            ret = thepage.save(content, summary=comment)

        return ret

    def replace_page(self, title, values={}, comment=""):
        """Replace the page with new values.
        """

        if self.site == None:
            return None
        else:
            thepage = self.site.Pages[title]
            content = thepage.edit()
            # replace new line with empty string.
            p = re.compile('\\n\|')
            onelineContent = p.sub('|', content)
            # get the template source in one line.
            p = re.compile('{{(.*)}}')
            temps = p.findall(onelineContent)
            oneline = temps[0]
            # replace | to \n as the standard template format.
            p = re.compile('\|')
            lines = p.sub('\\n|', oneline)
            # now for each new value to replace.
            for key, value in values.items():
                p = re.compile("""%s=.*""" % key)
                lines = p.sub("""%s=%s""" % (key, value), lines)
            # make the replaced content in one line too
            p = re.compile('\\n\|')
            replaced = p.sub('|', lines);
            onelineContent = onelineContent.replace(oneline, 
                                                    replaced)
            ret = thepage.save(onelineContent, summary=comment)
            return ret

    def template_values(self, filepath, pkg_name):
        """get ready all need values for the wiki template.
        """

        if self.headers_info == None:
            return None

        headers = self.extract_wp_headers(filepath)
        # adding the package name.
        headers['package_name'] = pkg_name
        for field_name, template in self.template_fields:
            field_value = template % headers
            headers[field_name] = field_value

        return headers

    def extract_wp_headers(self, filepath):
        """extract all WordPress file header fields from the given
        file. headers are configured in mw resource file,
        under [headers] section.
        """

        if self.headers_info == None:
            return None

        # return as a dict objet.
        ret = {}
        for field_name, pattern in self.headers_info:
            grep_pat = """grep -oE '%s' %s""" % (pattern, filepath)

            try:
                value = subprocess.check_output(grep_pat, shell=True)
                # only split the first ":"
                value = value.strip().split(b":", 1)
                ret[field_name] = value[1].strip()
            except subprocess.CalledProcessError:
                # could NOT find the pattern.
                if self.headers_default.has_key(field_name):
                    ret[field_name] = self.headers_default[field_name]
                else:
                    # empty string as the default.
                    ret[field_name] = ""

        return ret
