import sys
import os
import importlib

def isprivate(name):
    if name.startswith('_') and not name == '__init__':
        return True
    else:
        return False

def predicate(str):
    key, value = str.split(':')
    return lambda d: d[key] == value

def invert(fn):
    def inverted_fn(*args):
        return not fn(*args)
    return inverted_fn

def any(fns):
    def satisfy_any(*args):
        for fn in fns:
            if fn(*args):
                return True
        return False
    return satisfy_any

def load_path(path):
    directory = os.path.join(os.getcwd(), os.path.dirname(path))
    name = os.path.basename(os.path.splitext(path)[0])
    sys.path.insert(0, directory)
    module = importlib.import_module(name)
    sys.path.pop(0)
    return module