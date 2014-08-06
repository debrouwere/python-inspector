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

def factorize(a, b):
    return sum([a, b])
