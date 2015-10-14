# -*- coding: utf-8 -*-

# Small tools for converting between unicode and str.
#
# They are intended to be used in code that enables everyday code to deal with
# Unicode in a sane way. If you find yourself wanting to use them in everyday
# code, you should consider a different solution: can you write something that
# relieves the everyday code from dealing with Unicode explicitly? You may use
# these tools for writing that something, but not for the everyday code.

from __future__ import unicode
from warnings import warn

def utf8ify_if_unicode(x):
    """
    Turns unicode arguments into strs.

    When given a unicode argument, encodes it as UTF-8 str. Warns when given
    strs. Returns everything else unchanged.

    """
    if isinstance(x, unicode):
        return x.encode('utf-8')
    elif isinstance(x, str):
        warn(x + b" already is str. You should use unicode here!")
            # If the user gives a str, they probably don't know what they're
            # doing and want to get away with it.
        return x
    else:
        return x

def utf8ify_vals(d):
    """
    Encodes unicode values in a dictionary as UTF-8 strs.
    """
    return { k: utf8ify_if_unicode(v) for k, v in d.items() }

def utf8ify_dict(d):
    """
    Encodes unicode keys and values in a dictionary as UTF-8 strs.
    """
    return { utf8ify_if_unicode(k):
             utf8ify_if_unicode(v) for k, v in d.items() }

def unicodify_if_str(x):
    """
    Converts strs into unicodes and leaves everything else unchanged.

    Assumes strs to be UTF-8 encoded.
    """
    if isinstance(x, str):
        return x.decode('utf-8')
    elif isinstance(x, unicode):
        warn(x.encode('utf-8') + b" already is unicode. Why do you want to convert it?")
            # If the user gives a unicode, they probably don't know what
            # they're doing and want to get away with it.
        return x
    else:
        return x
