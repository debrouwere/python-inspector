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

def load_path(path):
    directory = os.path.join(os.getcwd(), os.path.dirname(path))
    # TODO: figure out a saner way to do this
    package = os.path.dirname(path).replace('/', '.')
    name = os.path.basename(os.path.splitext(path)[0])
    #sys.path.insert(0, directory)
    module = importlib.import_module(path)
    #sys.path.pop(0)
    return module

def render(__path, **kwargs):
    path = os.path.join(os.path.dirname(__file__), __path)
    return jinja2.Template(open(path).read()).render(**kwargs)
