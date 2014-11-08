""" File-level docs. """

class Bean(object):
    """ Documentation for beans. """

    def __init__(self, message):
        pass

    def cook(self, a, b=None):
        """ Some advice on how to cook a bean. """
        pass

    def crush(self, x=2):
        pass

class CoffeeBean(Bean):
    def cook(self, x=4):
        pass

    def roast(self, *vargs, **kwargs):
        pass



import functools
from decorator import decorator
import inspector

def functools_wrapper(fn):
    @functools.wraps(fn)
    def wrapped_fn(*vargs, **kwargs):
        fn(*vargs, **kwargs)
    return wrapped_fn

def decorator_wrapper(fn):
    @decorator
    def wrapped_fn(*vargs, **kwargs):
        fn(*vargs, **kwargs)
    return wrapped_fn

def inspector_wrapper(fn):
    @inspector.wraps(fn)
    def wrapped_fn(*vargs, **kwargs):
        fn(*vargs, **kwargs)
    return wrapped_fn


@functools_wrapper
def factorize1(a=[], b={}):
    """ Factorize functools """
    return sum([a, b])

#@decorator_wrapper
#def factorize2(a=[], b={}):
#    """ Factorize decorator """
#    return sum([a, b])

@inspector_wrapper
def factorize3(a=[], b={}):
    """ Factorize inspector """
    return sum([a, b])
