import functools


def wraps(wrapped, assigned=functools.WRAPPER_ASSIGNMENTS, updated=functools.WRAPPER_UPDATES, changes=False):
    def wrapper(fn):
        if not hasattr(fn, '__wraps__'):
            fn.__wraps__ = []
        fn.__wraps__.append(wrapped)
        if changes:
            fn.__original__ = fn
        else:
            fn.__original__ = wrapped
        functools.update_wrapper(fn, wrapped)
        return fn
    return wrapper

def changes(wrapped):
    return wraps(wrapped, changes=True)

def implements(wrapped):
    return wraps(wrapped, assigned=[], updated=[], changes=True)
