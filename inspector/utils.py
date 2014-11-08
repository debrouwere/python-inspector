import sys
import os
import importlib
import re
import jinja2

def property(key):
    return lambda d: d[key]

def predicate(string):
    if ':' in string:
        key, value = string.split(':')
        return lambda d: d[key] == value
    else:
        return property(string)

def find(l, **kwargs):
    for el in l:
        def match(item):
            return el.get(item[0]) == item[1]
        if all(map(match, kwargs.items())):
            return el
    return None

def index(l, test):
    for i, el in enumerate(l):
        if test(el):
            return i
    return None

def isprivate(name):
    if name.startswith('_') and not name == '__init__':
        return True
    else:
        return False

def unwrap(string):
    """ Keep double newlines as paragraph markers, 
    but get rid of any single newlines. """
    return re.sub(r'([^\n]+)\n', r'\1 ', string)

def load_path(path):
    directory = os.path.join(os.getcwd(), os.path.dirname(path))
    name = os.path.basename(os.path.splitext(path)[0])
    sys.path.insert(0, directory)
    module = importlib.import_module(name)
    sys.path.pop(0)
    return module

def render(__path, **kwargs):
    path = os.path.join(os.path.dirname(__file__), __path)
    return jinja2.Template(open(path).read()).render(**kwargs)
