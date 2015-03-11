import inspect
from . import utils


def identify(obj, parent=None, name=None):
    if hasattr(obj, '__name__'):
        properties = {
            'name': name, 
            'identity': obj.__name__, 
            # TODO: look for a better solution
            'module': getattr(inspect.getmodule(obj), '__name__', ''), 
            'documentation': inspect.getdoc(obj), 
        }
    else:
        properties = {
            'name': name, 
            'identity': name, 
            'type': 'attribute', 
            'documentation': None, 
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

    if hasattr(obj, '__wraps__'):
        properties['wraps'] = obj.__wraps__
        if len(properties['wraps']):
            properties['wrapped'] = True
    else:
        properties['wraps'] = []
        properties['wrapped'] = False

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
            'repr': '*' + signature.varargs, 
            'type': 'variable', 
        })

    if signature.keywords:
        arguments.append({
            'name': signature.keywords, 
            'repr': '**' + signature.keywords, 
            'type': 'keywords', 
        })

    return arguments

def describe(obj, parent=None, name=None):
    properties = identify(obj, parent, name)

    if inspect.isclass(obj) or inspect.ismodule(obj):
        properties['members'] = [describe(member, properties, name) 
            for name, member in inspect.getmembers(obj)
            if not inspect.isbuiltin(member) 
            and not utils.isprivate(name) 
            and not inspect.ismodule(member)]

    if inspect.isclass(obj):
        init_ix = utils.index(properties['members'], 
            lambda member: member['name'] == '__init__')

        if init_ix:
            # pop init from the members
            # (it is listed at the class level instead)
            init = properties['members'].pop(init_ix)
            signature = init['signature']
            properties['call'] =  '{name}({call})'.format(
                name=properties['name'], call=signature)
        else:
            properties['call'] = '{name}()'.format(name=properties['name'])

    elif inspect.ismethod(obj) or inspect.isfunction(obj):
        if hasattr(obj, '__original__'):
            original = obj.__original__
        else:
            original = obj

        raw_arguments = describe_function(obj)
        properties['arguments'] = arguments = describe_function(original)

        if 'wraps' in properties:
            properties['wraps'] = [describe_function(wrapped) for wrapped in properties['wraps']]
            if inspect.ismethod(obj):
                properties['wraps'] = [arguments[1:] for arguments in properties['wraps']]

        # skip self
        if inspect.ismethod(obj):
            arguments = arguments[1:]

        def to_signature(arguments):
            return ", ".join([argument['repr'] for argument in arguments])

        def to_call(arguments):
            signature = to_signature(arguments)
            return '{name}({signature})'.format(
                name=properties['name'], signature=signature)

        properties['signature'] = to_signature(arguments)
        properties['call'] = to_call(arguments)
        raw_signature = to_signature(raw_arguments)
        raw_call = to_call(raw_arguments)
        properties['signatures'] = [raw_signature] + \
            [to_signature(arguments) for arguments in properties['wraps']]
        properties['calls'] = [raw_call] + \
            [to_call(arguments) for arguments in properties['wraps']]

    documented_members = any(map(utils.property('documentation'), properties.get('members', [])))
    documented_self = properties['documentation']
    properties['documented'] = bool(documented_members or documented_self) is True

    return properties
