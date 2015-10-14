# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import argparse

class ArgumentParser(object):
    """
    An argparse.ArgumentParser, just with unicode instead of str output.

    If you don't provide the ``type`` argument to
    ``argparse.ArgumentParser.add_argument``, it assumes that the value of
    this argument should be returned as str. This class wraps ArgumentParser
    in order to make the default return type unicode.

    Note that this can't be achieved just by specifying ``type=unicode``,
    since that way non-ASCII characters in command line arguments would cause
    problems. Even with this class, this is the case. I could have written it
    in a way that if you say ``type=unicode``, it would automatically handle
    non-ASCII characters. However, this would be inconsistent with the API of
    argparse.ArgumentParser, which expect the ``type`` argument to be a
    function and not some keyword triggering behind-the-scenes stuff. Tell me
    if you find this reasoning silly.
    """

    def __init__(self, *args, **kwargs):
        self.arg_parser = argparse.ArgumentParser(*args, **kwargs)

        # Note that this takes [str] as the first argument.
        self.parse_args = self.arg_parser.parse_args

    def add_argument(self, *args, **kwargs):
        if kwargs.get('action', 'store') in ['store', 'append'] \
                and 'type' not in kwargs:
            kwargs['type'] = lambda s: s.decode('utf-8')

        return self.arg_parser.add_argument(*args, **kwargs)
