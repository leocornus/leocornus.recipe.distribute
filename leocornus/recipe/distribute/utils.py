# utils.py

# save some utility functions here.

import os
import re
import subprocess
import mwclient
try:
    import ConfigParser as configparser
except ImportError:
    import configparser

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

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
        self.mw_info = {}
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
            # needs the set the raw to True
            self.templates = dict(rc.items('template', True))
            self.template_fields = rc.items('template fields', True)
            self.mw_info = dict(rc.items('mwclient'))
            if not self.mw_info.has_key('update_wiki'):
                # update_wiki not set, give the default value.
                self.mw_info['update_wiki'] = 'no'
            if self.mw_info['update_wiki'] == 'yes':
                # try to create the mwclient site instance.
                self.site = mwclient.Site(self.mw_info['host'], 
                                          path=self.mw_info['path'])
                self.site.login(self.mw_info['username'], 
                                self.mw_info['password'])
        else:
            # need set up the default values for header info.
            # only need version.
            self.headers_info = [('latest_version', 'Version:.*')]
            # set update _wiki to no
            self.mw_info['update_wiki'] = 'no'

    def update_wiki(self, values):
        """Update wiki based on the given values.
        """

        ret = {}
        # check the update_wiki option.
        if self.mw_info['update_wiki'] != "yes":
            # wiki access not configured, skip.
            ret['status'] = 'skip'
            ret['message'] = 'Wiki update is OFF'
            return ret

        # we should have site already, let's start the wiki update.
        # 1. get ready the title and comment
        title = values['title']
        comment = values['comment']
        # 2. page content will depend on the page exist or not!
        thepage = self.site.Pages[title]
        if thepage.exists:
            wiki_ret = self.replace_page(thepage, values, comment)
            wiki_ret['action'] = 'update'
        else: 
            # create new page.
            wiki_template = self.templates['wiki_template']
            content = wiki_template % values
            wiki_ret = self.create_page(title, content, comment)
            wiki_ret['action'] = 'create'
        # wrap up the wiki return
        ret['status'] = "[%(action)s: %(result)s]" % wiki_ret
        ret['message'] = "Page Title: %(title)s" % wiki_ret
        return ret

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

    def replace_page(self, thepage, values={}, comment=""):
        """Replace the page with new values.
        we will only process the template content and leave
        other content as it is.
        """

        # the original conent.
        org_content = thepage.edit()
        # get template name from values.
        p = re.compile("{{(%s.*)}}" % values['template_name'],
                       re.DOTALL)
        # try to find the template content.
        matches = p.findall(org_content)
        if len(matches) == 0:
            # no template exist! add the template at beginning.
            tpl_content = self.templates['wiki_template'] % values
            new_content = "%s\n%s" % (tpl_content, org_content)
        else:
            # only handle the first match.
            # the original template content
            org_tpl_content = matches[0]
            # replace new line with empty string.
            p = re.compile('\\n\|')
            oneline_content = p.sub('|', org_tpl_content)
            # replace | to \n as the standard template format.
            p = re.compile('\|')
            new_tpl_content = p.sub('\\n|', oneline_content)
            # now for each new value to replace.
            for key, value in values.items():
                p = re.compile("""%s[\s]*=.*""" % key)
                new_tpl_content = p.sub("""%s=%s""" % (key, value), 
                                        new_tpl_content)

            # replace the original conent with new standard content.
            new_content = org_content.replace(org_tpl_content, 
                                              new_tpl_content)

        # save the new content back only it is changned.
        if org_content == new_content:
            # skip 
            ret = {"result": "No Change", "title": thepage.name}
        else:
            # save it with comment.
            ret = thepage.save(new_content, summary=comment)

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
                # we only handle the first occurance, to avoid the
                # duplicate header pattern issue.
                value = value.splitlines()[0]
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
