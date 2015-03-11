"""
Inspect.

When documenting a library or software product written in Python, often 
a README is not enough, but full-blown Sphinx is too much work or too rigid.

Inspect is a command-line tool that will automatically document Python code, 
but it returns the output as machine-readable JSON or human-readable Markdown, 
so you retain full control of how to render the documentation.

Usage:
    inspect <path> [<object>] [options]

Options:
    -m --markdown <level>   At what level to start headers [3].
    --include <includes>    ...
    --exclude <excludes>    ...

If you only need a single object documented (whether a function, a class 
or something else), you can use the <object> argument:

    # will only include documentation on `A`
    inspect fixtures/example.py A

Filtering the output with `--include` and `--exclude` ensures that your code 
description only contains exactly what you want it to. Some examples: 

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

As you can see, `.` traverses the hierarchy and `:` is the value to test 
against. (If you don't specify a value, we will test on presence.)

`,` separates multiple criteria that are OR'ed together.

Todo:

* improve documentation
* unit test the filtering mechanism
* fill out missing information in the description JSON (if any)
* an `intercalate` utility that runs shell commands inside of `%%` tags
  in a file and replaces the tags with the standard output from those
  commands
"""

import json
import itertools
import jinja2
import docopt
from . import utils
from . import filters
from .describe import describe
from .annotators import wraps, changes, implements


def cli():
    arguments = docopt.docopt(__doc__, version='inspect 0.1')

    module = utils.load_path(arguments['<path>'])
    if arguments['<object>']:
        obj = getattr(module, arguments['<object>'])
    else:
        obj = module
    description = describe(obj, parent=module, name=arguments['<object>'])

    include = arguments['--include'] or ''
    exclude = arguments['--exclude'] or ''
    criteria = (include + ' ' + exclude).strip().split(',')
    grouped_criteria = {}
    for group, values in itertools.groupby(criteria, lambda criterion: len(criterion.split('.'))):
        grouped_criteria[group] = list(values)
    global_criteria = filter(bool, grouped_criteria.get(1, []))
    local_criteria = filter(bool, grouped_criteria.get(2, []))
    local_criteria = [criterion.split('.') for criterion in local_criteria]
    grouped_local_criteria = dict(
        itertools.groupby(local_criteria, lambda criterion: criterion[0]))

    if global_criteria:
        description['members'] = filters.filter(
            global_criteria, description['members'], invert=exclude)

    if local_criteria:
        for prop, criteria in grouped_local_criteria.items():
            criteria = map(lambda criterion: criterion[1], criteria)
            for obj in description['members']:
                if prop in obj:
                    obj[prop] = filters.filter(
                        criteria, obj[prop], invert=exclude)

    if arguments['--markdown']:
        root = int(arguments['--markdown'])
        header = "".join(['#' for level in range(root)])
        print(utils.render('markdown.html.j2', header=header, **description))
    else:
        print(json.dumps(description, indent=4))
