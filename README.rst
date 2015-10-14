==============================================================
As Short as Possible Guidelines for Handling Unicode in Python
==============================================================

Conventions (recommended)
=========================

 - Write ``unicode`` or unicode if you mean the Python type.
 - Write Unicode if you mean Unicode in general.

Need to Know (mandatory)
========================

❃ ``str`` vs. ``unicode`` vs. ``bytes`` and Python 2 vs. Python 3
    When dealing with strings and Unicode in Python, there are two types
    you have to know. ``str`` is a plain list of bytes that just happens to
    be rendered as a string. ``unicode`` is a list of Unicode characters.
    Python 2 → Python 3: ``str`` → ``bytes``, ``unicode`` → ``str``.

❃ default string type
    The default string type in both Pythons is ``str``, but note that ``str``
    is different things in Python 2 and Python 3. In Python 3 all string
    variables inside a program are lists of Unicode characters and we
    want to have the same in Python 2, because we are forward-looking.

❃ every string is ``unicode``
    Therefore, we assume all string variables inside our programs to be
    of type ``unicode``.

❃ (nearly) everything outside is ``str``
    When communicating with the outside world and some libraries, we have
    to convert to or from ``str``.

❃ Unicode and UTF-8
    Unicode is different from UTF-8. Read the first paragraph in the blue
    box at the top of
    https://pythonhosted.org/kitchen/unicode-frustrations.html.

❃ encoding and decoding
    To turn a UTF-8-encoded ``str`` (list of bytes) into ``unicode``, use
    ``.decode('utf-8')``. To turn a ``unicode`` into a UTF-8-encoded ``str``,
    use ``.encode('utf-8')``.

Rules (mandatory)
=================

❃ unicode_literals
    In every Python file, import ``unicode_literals``::

        from __future__ import unicode_literals

    If you don't do this, all string literals in your source code will be
    ``str``, which is against the »every string is ``unicode``\« of the Need
    to Know.

❃ ``str`` literals
    Use ``b"bla"`` to write a ``str`` "bla".

❃ string conversion
    Use ``unicode()`` instead of ``str()`` when you want to convert numbers
    etc. to strings.

❃ naming convention
    If there is a string variable that needs to be of type ``str`` inside
    your program, prefix it with ``b_`` if you don't know the encoding or
    with ``utf8_`` if you know it is UTF-8.

❃ Git SHA1s
    Git SHA1s as returned by ``Oid.hex`` are of type ``str``. Since they never
    contain non-ASCII characters and it would be annoying to convert them all
    the time, we leave them as ``str``. Since we know that they are ``str``
    and it is annoying to write prefixes, it is okay to leave off the ``b_``.
    (Not so sure if this is good, though.)

❃ reading and writing files
    When you want to read from or write to a file, use ``codecs.open()``::

        >>> from __future__ import unicode_literals
        >>> import codecs
        >>> with codecs.open("bla.txt", 'w', 'utf-8') as f:
        ...     f.write("üüü")
        ...
        >>> with codecs.open("bla.txt", 'r', 'utf-8') as f:
        ...     f.read(3)
        ...
        u'\xfc\xfc\xfc'
        >>> 'ü' * 3
        u'\xfc\xfc\xfc'

❃ ``print``
    Everything that is written to the outside world should be ``str``. This
    includes parameters to ``print``. Write at the top of every file, but
    after all imports::

        if not isinstance(sys.stdout, codecs.StreamWriter):
            sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

    (Don't forget to add imports for ``sys`` and ``codecs`` if they aren't
    there already.) This way you can do ``print(unicode)``. Note however, that
    now it's dangerous to do ``print(str)``. Never pass a ``str`` to ``print``
    unless you're sure it contains only ASCII. In such cases, write a
    clarifying comment.

❃ exceptions and warnings
    When raising exceptions or warnings, only pass ``str``. Think twice whether
    the thing you're passing really is ``str``!

❃ ``print`` to ``sys.stderr``
    We don't put an UTF-8 writer in front of ``sys.stderr``, since that would
    cause even more confusion. So make sure that everything you send there is
    ``str``.

❃ external libraries
    Check whether the library calls you're using accept and return ``str`` or
    ``unicode``. If they accept and return ``str``, take care to make the
    right conversions. Below are my `notes on which libraries do what`_.

❃ environment variables
    Use ``unicode_environ.getenv`` and ``unicode_environ.environ`` instead of
    ``os.getenv`` and ``os.environ``. If you need to do anything else with the
    environment, extend ``unicode_environ`` instead of resorting to
    environment utilities from ``os``.

❃ command line arguments
    Command line arguments come as ``str`` and you need to convert them.
    Unfortunately, passing ``type=unicode`` to ``ArgumentParser.add_argument``
    is not enough. Use ``unicode_argparse.ArgumentParser`` instead of
    ``argparse.ArgumentParser``.

❃ testing
    In your tests, try to break the system by including non-ASCII characters
    in strings. If you can't succeed, chances are good that you have done the
    Unicode thing correctly.

❃ CONSTANT VIGILANCE!
    When you read data from or write data to somewhere outside your program,
    make sure it gets converted to the right types.

Recommendations (recommended)
=============================

❃ UTF-8-encoded source
    In the first or second line of every Python file, put the following:

        # -*- coding: utf-8 -*-

    Doing this will allow you to use non-ASCII characters in your Python
    source.

❃ writing Unicode utilities
    If you want to write utilities like ``unicode_environ`` and
    ``unicode_argparse``, you might find the functions from ``unicode_tools``
    helpful.

.. I couldn't figure out how to do the internal linking right. X(

.. _notes on which libraries do what:

Does library ``x`` use ``unicode`` or ``str``?
==============================================

When I write something like »works with ``unicode`` arguments«, I mean that it
works with arguments of type ``unicode`` which can contain arbitrary
characters, i. e. ASCII as well as non-ASCII.

Feel free to extend.

codecs
------

``codecs.open`` works with ``unicode`` as well as ``str`` filenames.

datetime
--------

``datetime.datetime.strftime(unicode)``: ``str``

httplib2
--------

``httplib2.Http.request`` works with ``unicode`` arguments. However, the
results will all contain or be of type ``str``. Example:

    >>> r, c = httplib2.Http(".cache").request("http://de.wikipedia.org/wiki/Erdkröte")
    >>> r['content-type']
    'text/html; charset=UTF-8'
    >>> type(r['content-type'])
    <type 'str'>
    >>> type(c)
    <type 'str'>

os.path
-------

Things in os are generally safe to use with ``unicode``. However, note this:

 - ``path.join(unicode, unicode)``: ``unicode``
 - ``path.relpath(unicode, unicode)``: ``str`` or ``unicode`` (!!!)
   If the result contains non-ASCII characters, it will be ``unicode``,
   otherwise ``str``. Isn't it sweet?

PycUrl
------

PyCurl works solely on ``str``\s.

Pygit2
------

 - Config values can be ``unicode``.
 - ``Commit.hex``: ``str``
 - ``Commit.message``: ``unicode``
 - Paths are ``str``. However, this is extrapolated from the fact that
   ``Patch.delta.{old,new}_file.path`` is ``str``. The API might be
   inconsistent, so check the thing you're using and add the data here.
 - ``Reference.name``, ``Reference.shorthand``: ``str``
 - However, ``Repository.lookup_reference(unicode)`` works.
 - Refspecs should be ``str``. ``Remote.add_fetch`` doesn't complain when you
   pass ``unicode``, but ``Remote.fetch_refspecs`` throws an exception if you
   added a refspec with non-ASCII characters. Funny enough, though,
   ``Remote.fetch_refspecs`` is an list of ``unicode``.
 - ``Repository(path)`` doesn't work with ``unicode``\s containing non-ASCII
   characters. To be sure I'd say that all paths passed to Pygit2 methods or
   the like should be converted to UTF-8 ``str``\s first.
 - ``Signature.name``, ``Signature.email``: ``unicode``. If you need ``str``,
   you can use ``Signature.raw_name`` and ``Signature.raw_email``.

Trivia::

    >>> no_r = pygit2.Repository("/tmp/tüüls")               # throws error
    >>> r = pygit2.clone_repository("/tmp/tüüls", "./tüüls") # works
    >>> r.remotes[0].url                                     # throws error

re
--

re is completely okay with ``unicode`` everywhere.

Textile
-------

``textile.textile`` returns ``unicode`` if you give it ``unicode``.

urllib(2)
---------

urllib2 didn't like ``unicode`` for URLs and also returned ``str`` only. Since
urllib is older, I guess it's the same there.

Resources (recommended)
=======================

 - https://docs.python.org/2.7/howto/unicode.html
 - https://pythonhosted.org/kitchen/unicode-frustrations.html
 - http://python-future.org/unicode_literals.html
 - the documentation of the mentioned modules or libraries

Todo (recommended)
==================

If you are in an industrious mood, you can help improving this document.

 - I marked up many things as ``literal text``. It would be nice if you
   could change this to interpreted text, such as
   :meth:`pygit2.Diff.merge`. But you'd also have to find the right way
   to convert this to HTML, since rst2html doesn't like ``meth`` (as
   well as the other Python-specific roles, I guess).
