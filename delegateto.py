def delegate(to, *methods):
    """
    Class decorator to delegate methods to another objects.
    >>> @delegate('v', 'upper')
    ... @delegate('v', 'lower')
    ... @delegate('v', 'wrong_method')
    ... @delegate('not_an_attribute', 'wrong_attribute')
    ... class Foo:
    ...     def __init__(self, v):
    ...         self.v = v
    >>>
    >>> Foo('foo').upper()
    'FOO'
    >>> Foo('FOO').lower()
    'foo'

    >>> Foo('foo').wrong_method()
    Traceback (most recent call last):
        ...
    AttributeError: 'str' object has no attribute 'wrong_method'

    >>> Foo('foo').wrong_attribute()
    Traceback (most recent call last):
        ...
    AttributeError: 'Foo' object has no attribute 'not_an_attribute'

    You can use pass any number of methods to delegate
    >>> @delegate('v', 'upper', 'lower')
    ... class Foo:
    ...     def __init__(self, v):
    ...         self.v = v

    Properties can also be delegated.
    >>> class Bar:
    ...     def __init__(self):
    ...         self._param = 0
    ...     @property
    ...     def param(self):
    ...         return self._param
    ...     @param.setter
    ...     def param(self, param):
    ...         self._param = param

    >>> @delegate('v', 'param')
    ... class Foo2:
    ...     def __init__(self):
    ...         self.v = Bar()

    >>> foo2 = Foo2()

    >>> foo2.param
    0
    >>> foo2.param = 2
    >>> foo2.param
    2
    >>> foo2.v.param
    2
    >>> foo2.v._param
    2
    """

    def dec(klass):
        for m in methods:
            setattr(klass, m, DelegateTo(to, m))
        return klass

    return dec


class DelegateTo:
    """
    DelegateTo descriptor let you delegate method calls

    The argument name is the name of the method that you want to
    delegate, for example.
    >>> class Foo:
    ...     upper = DelegateTo('v')
    ...     __len__ = DelegateTo('l')
    ...     __iter__ = DelegateTo('l')
    ...     def __init__(self, v, l):
    ...         self.v = v
    ...         self.l = l
    >>> foo = Foo('hello world', [1, 2, 3])

    To call a method just call its delegator
    >>> foo.upper()
    'HELLO WORLD'

    Magic methods are supported
    >>> len(foo)
    3
    >>> [x*2 for x in foo]
    [2, 4, 6]

    The method name is discovered at the first call. This
    is done by iterating over all the object's attributes.
    Once found the method is cached and no search is
    performed in the subsequent calls.

    Still, if you need to avoid this iteration you can initialize
    the method name with the same name of the attibute name.
    For example
    >>> class Foo:
    ...     upper = DelegateTo('v', 'upper')
    ...     def __init__(self, v):
    ...         self.v = v


    Also is possible to use this to create aliases
    >>> class Foo:
    ...     up = DelegateTo('v', 'upper')
    ...     def __init__(self, v):
    ...         self.v = v
    >>> Foo('hello').up()
    'HELLO'

    In this context 'self' has a special meaning of
    delegating a method to another method in the same
    object. For example
    >>> class Foo:
    ...     foo = DelegateTo('self', 'bar')
    ...     def bar(self):
    ...         return 'bar'
    >>> Foo().foo()
    'bar'
    """

    def __init__(self, to, method=None):
        if to == "self" and method is None:
            raise ValueError("DelegateTo('self') is invalid, " "provide 'method' too")
        self.to = to
        self.method = method

    def __get__(self, obj, objtype):
        if self.to == "self":
            return getattr(obj, self.method)
        if self.method is not None:
            return getattr(getattr(obj, self.to), self.method)
        for method, v in obj.__class__.__dict__.items():
            if v is self:
                self.method = method
                return getattr(getattr(obj, self.to), method)

    def __set__(self, obj, value):
        setattr(getattr(obj, self.to), self.method, value)


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=2)
