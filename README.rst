Inspect.

When documenting a library or software product written in Python, often
a README is not enough, but full-blown Sphinx is too much work or too
rigid.

Inspect is a command-line tool that will automatically document Python
code, but it returns the output as machine-readable JSON or
human-readable Markdown, so you retain full control of how to render the
documentation.

Usage: inspect [] [options]

Options: -m --markdown At what level to start headers. --include ...
--exclude ...

If you only need a single object documented (whether a function, a class
or something else), you can use the

.. raw:: html

   <object> 

argument:

::

    # will only include documentation on `A`
    inspect fixtures/example.py A

Filtering the output with ``--include`` and ``--exclude`` ensures that
your code description only contains exactly what you want it to. Some
examples:

::

    # only include class methods if they've been documented
    inspect fixtures/example.py --include members.documented
    # only include classes
    inspect fixtures/example.py --include type:class
    # only document function `factorize` and class `Bean`
    inspect fixtures/example.py --include name:fun,name:B
    # only include documented methods on Bean
    # (these two are identical)
    inspect fixtures/example.py Bean --include documented
    inspect fixtures/example.py --include name:Bean,members.documented

As you can see, ``.`` traverses the hierarchy and ``:`` is the value to
test against. (If you don't specify a value, we will test on presence.)

``,`` separates multiple criteria that are OR'ed together.

Todo:

-  improve documentation
-  unit test the filtering mechanism
-  fill out missing information in the description JSON (if any)
-  an ``intercalate`` utility that runs shell commands inside of ``%%``
   tags in a file and replaces the tags with the standard output from
   those commands

