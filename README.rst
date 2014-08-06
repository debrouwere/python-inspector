Inspect.

When documenting a library or software product written in Python, often
a README is not enough, but full-blown Sphinx is too much work or too
rigid.

Inspect is a command-line tool that will automatically document Python
code, but it returns the output as JSON or Markdown so you retain full
control of how to render the documentation.

Usage: inspect [] [options]

Options: --include --exclude

Todo:

-  improve documentation
-  fill out missing information in the description JSON (if any)
-  output to Markdown
-  an ``intercalate`` utility that runs shell commands inside of ``%%``
   tags in a file and replaces the tags with the standard output from
   those commands

