# utils.py

# save some utility functions here.

import subprocess

def extractHeader(pattern, fullFilePath, default):
    """extract header field values from the given file.
    """
    grepPattern = """grep -oE '%s' %s""" % (pattern, fullFilePath)
    try:
        ret = subprocess.check_output(grepPattern, shell=True)
        # only split the first ":"!
        ret = ret.strip().split(b":", 1)
        return ret[1].strip()
    except subprocess.CalledProcessError:
        # could not find the pattern, return default value?
        return default
