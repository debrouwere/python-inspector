"""
Inspect.

When documenting a library or software product written in Python, often 
a README is not enough, but full-blown Sphinx is too much work or too rigid.

Inspect is a command-line tool that will automatically document Python code, 
but it returns the output as JSON or Markdown so you retain full control of 
how to render the documentation.

Usage:
    inspect <path> [<object>] [options]

Options:
    --include <predicates...>
    --exclude <predicates...>

Todo:

* improve documentation
* fill out missing information in the description JSON (if any)
* output to Markdown
* an `intercalate` utility that runs shell commands inside of `%%` tags
  in a file and replaces the tags with the standard output from those
  commands
"""

from docopt import docopt
import inspect
import json
import utils

def identify(obj, parent=None):
    name = obj.__name__
    properties = {
        'name': name, 
        'module': inspect.getmodule(obj).__name__, 
        'documentation': inspect.getdoc(obj), 
    }

    if hasattr(obj, '__file__'):
        properties['path'] = obj.__file__.replace('.pyc', '.py')

    if inspect.isclass(obj):
        properties['type'] = 'class'
        properties['repr'] = 'class ' + name
    elif inspect.isfunction(obj):
        properties['type'] = 'function'
        properties['repr'] = name
    elif inspect.ismethod(obj):
        properties['type'] = 'method'
        properties['repr'] = '{parent}#{name}'.format(
            parent=parent['name'], name=name)

    return properties

def describe_function(fn):
    arguments = []
    signature = inspect.getargspec(fn)
    defaults = list(signature.defaults or [])

    for i, name in enumerate(signature.args):
        left = len(signature.args) - i

        argument = {
            'name': name, 
            'repr': name, 
            'type': 'positional', 
        }

        if left <= len(defaults):
            default = defaults.pop()
            argument['default'] = default
            argument['repr'] = '{repr}={default}'.format(**argument)

        arguments.append(argument)

    if signature.varargs:
        arguments.append({
            'name': signature.varargs, 
            'repr': '*' + signature.keywords, 
            'type': 'variable', 
        })

    if signature.keywords:
        arguments.append({
            'name': signature.keywords, 
            'repr': '**' + signature.keywords, 
            'type': 'keywords', 
        })

    return arguments

def describe(obj, parent=None):
    properties = identify(obj, parent)

    if inspect.isclass(obj) or inspect.ismodule(obj):
        properties['members'] = [describe(member, properties) 
            for name, member in inspect.getmembers(obj)
            if not inspect.isbuiltin(member) and not utils.isprivate(name)]

    if inspect.isclass(obj):
        has_init = len([member for member in properties['members'] 
            if member['name'] == '__init__'])

        if has_init:
            # pop init from the members
            # (it is listed at the class level instead)
            init = properties['members'].pop(0)
            signature = init['signature']
            properties['call'] =  '{name}({call})'.format(
                name=properties['name'], call=signature)
        else:
            properties['call'] = '{name}()'.format(name=properties['name'])
    elif inspect.ismethod(obj) or inspect.isfunction(obj):
        properties['arguments'] = arguments = describe_function(obj)

        # skip self
        if inspect.ismethod(obj):
            arguments = arguments[1:]

        properties['signature'] = signature = \
            ", ".join([argument['repr'] for argument in arguments])
        properties['call'] = '{name}({signature})'.format(
            name=properties['name'], signature=signature)

    return properties


def cli():
    arguments = docopt(__doc__, version='inspect 0.1')
    module = utils.load_path(arguments['<path>'])
    if arguments['<object>']:
        module = getattr(module, arguments['<object>'])
    description = describe(module)

    include = arguments['--include'] or ''
    exclude = arguments['--exclude'] or ''
    criteria = (include + ' ' + exclude).strip()

    if criteria:
        includes = map(utils.predicate, criteria.split(' '))
        matcher = utils.any(includes)
        if exclude:
            matcher = utils.invert(matcher)
        description['members'] = filter(matcher, description['members'])

    print json.dumps(description, indent=4)
