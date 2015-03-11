from . import utils

# Python 2 and 3 compatibility
try:
    import builtins
except ImportError:
    import __builtin__ as builtins


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

def filter(criteria, obj, invert=False):
    includes = map(utils.predicate, criteria)
    matcher = any(includes)
    if invert:
        matcher = invert(matcher)
    return builtins.filter(matcher, obj)

def include(criteria, obj):
    return filter(criteria, obj)

def exclude(criteria, obj):
    return filter(criteria, obj, invert=True)
