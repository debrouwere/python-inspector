""" File-level docs. """

class A(object):
    """ Some docs. """

    def __init__(self, message):
        pass

    def method(self, a, b=None):
        """ Docs on A.method """
        pass

    def overridable(self, x=2):
        pass

class B(A):
    def overridable(self, x=4):
        pass

    def submethod(self, *vargs, **kwargs):
        pass

def fun(a, b):
    return sum([a, b])
