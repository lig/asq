'''Python 2 and Python 3 compatibility'''

import sys
import six


six.add_move(six.MovedAttribute(
    'zip_longest', 'itertools', 'itertools', 'izip_longest', 'zip_longest'))

is_callable = six.callable
itervalues = six.itervalues
iteritems = six.iteritems

imap = six.moves.map
ifilter = six.moves.filter
izip = six.moves.zip
izip_longest = six.moves.zip_longest
irange = six.moves.xrange
fold = six.moves.reduce

function_name = lambda f: six.get_function_code(f).co_name
has_unicode_type = lambda: not six.PY3
is_string = lambda s: isinstance(s, six.string_types)

try:
    from collections import OrderedDict
except ImportError:
    try:
        from ordereddict import OrderedDict
    except ImportError:
        sys.stderr.write(
            'Could not import OrderedDict. For Python versions earlier than'
            ' 2.7 install the ordereddict module from the Python Package Index'
            ' with easy_install ordereddict.')
        sys.exit(1)

try:
    # Python 2.7+ and Python 3.2+
    from functools import total_ordering as totally_ordered
except ImportError:
    # Python 2.6 version from
    # http://code.activestate.com/recipes/576685-total-ordering-class-decorator/
    # This recipe doesn't actually work on Python 3.0 or 3.1 but that doesn't
    # matter since neither of those implementations cause the
    # extra methods added by the decorator to be exercised.  This may become
    # an issue in future if somebody creates an alternative Python 3
    # implementation which is not up to Python 3.2 completeness.  That seems
    # unlikely.
    def totally_ordered(cls):
        'Class decorator that fills-in missing ordering methods'
        convert = {
            '__lt__': [('__gt__', lambda self, other: other < self),
                       ('__le__', lambda self, other: not other < self),
                       ('__ge__', lambda self, other: not self < other)],
            '__le__': [('__ge__', lambda self, other: other <= self),
                       ('__lt__', lambda self, other: not other <= self),
                       ('__gt__', lambda self, other: not self <= other)],
            '__gt__': [('__lt__', lambda self, other: other > self),
                       ('__ge__', lambda self, other: not other > self),
                       ('__le__', lambda self, other: not self > other)],
            '__ge__': [('__le__', lambda self, other: other >= self),
                       ('__gt__', lambda self, other: not other >= self),
                       ('__lt__', lambda self, other: not self >= other)]
        }
        if hasattr(object, '__lt__'):
            roots = [op for op in convert if getattr(cls, op) is not getattr(object, op)]
        else:
            roots = set(dir(cls)) & set(convert)
        assert roots, 'must define at least one ordering operation: < > <= >='
        root = max(roots)       # prefer __lt __ to __le__ to __gt__ to __ge__
        for opname, opfunc in convert[root]:
            if opname not in roots:
                opfunc.__name__ = opname
                opfunc.__doc__ = getattr(int, opname).__doc__
                setattr(cls, opname, opfunc)
        return cls
