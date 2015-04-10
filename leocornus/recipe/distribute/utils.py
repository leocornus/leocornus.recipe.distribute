# utils.py

# save some utility functions here.

import subprocess

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
