# -*- coding: utf-8 -*-

# Wrappers for os.getenv and os.environ that return unicode instead of str
# values.
#
# You can use unicode_environ.environ as drop-in replacement for
# os.environ as long as you only perform dictionary lookups and stores. If you
# want to do something else, please extend UnicodeEnviron.

from __future__ import unicode_literals
import os

import unicode_tools as ut

class UnicodeEnviron(object):
    def __contains__(self, key):
        return os.environ.__contains__(ut.utf8ify_if_unicode(key))

    def __getitem__(self, key):
        return ut.unicodify_if_str( os.environ[key] )

    def __setitem__(self, key, value):
        os.environ[key] = ut.utf8ify_if_unicode(value)

environ = UnicodeEnviron()

def getenv(key, default=None):
    val = os.getenv(key) # I know getenv(key, default), but we only want to
                         # unicodify the val and not the default.

    if val is None:
        return default
    else:
        return ut.unicodify_if_str(val)
