[![Build Status](https://travis-ci.org/dhilst/delegate.svg?branch=master)](https://travis-ci.org/dhilst/delegate)
# Delegate methods made easy

This tiny library implements two simple ways of method or property delegators, by descriptors
and by class decorators.

From wikipedia, what is delegation:
> In object-oriented programming, delegation refers to evaluating a member
> (property or method) of one object (the receiver) in the context of another
> original object (the sender). Delegation can be done explicitly, by passing
> the sending object to the receiving object, which can be done in any
> object-oriented language; or implicitly, by the member lookup rules of the
> language, which requires language support for the feature.

# Installation

This is python3 only, but it's very simple library with no dependences, it would not be hard to port it to python2, contributions are welcome!

    pip install delegateto

# Examples

DelegateTo descriptor let you delegate method or property calls

The argument name is the name of the method or property that you want to
delegate, for example.

    from delegateto import DelegateTo
    class Foo:
        upper = DelegateTo('v')
        __len__ = DelegateTo('l')
        __iter__ = DelegateTo('l')

        def __init__(self, v, l):
            self.v = v
            self.l = l

    foo = Foo('hello world', [1, 2, 3])

To call a method just call its delegator

    foo.up() # => 'HELLO WORLD'

Magic methods are supported

    len(foo) # => 3
    [x*2 for x in foo] # => [2, 4, 6]


At class parsing time is not possible for `DelegateTo` to know to what 
attribute you're assigning it to. For example `foo = DelegateTo('bar')` Pay 
attention that `DelegateTo` doesn't receive any information about `foo` 
attribute, but it will discover this latter.  The method name is discovered at 
the first call. This is done by iterating over all the object's attributes. 
Once found the method is cached and no search is performed in the subsequent 
calls.

Still, if you need to avoid this iteration you can initialize 
the method name with the same name of the attribute name. 

For example

    class Foo:
        upper = DelegateTo('v', 'upper')
        def __init__(self, v):
            self.v = v


This make possible the creation of aliases

    class Foo:
        up = DelegateTo('v', 'upper')
        def __init__(self, v):
            self.v = v

    Foo('hello').upper() # => 'HELLO'

In this context 'self' has a special meaning of 
delegating a method to another method in the same 
object. For example 

    class Foo:
        foo = DelegateTo('self', 'bar')
        def bar(self):
            return 'bar'

    Foo().foo() # => 'bar'


There is another way of creating delegators with class decorators, here is how 

    from delegateto import delegate
    @delegate('v', 'upper')
    @delegate('v', 'lower')
    @delegate('v', 'wrong_method')
    @delegate('not_an_attribute', 'wrong_attribute')
    class Foo:
        def __init__(self, v):
            self.v = v

    Foo('foo').upper() # => 'FOO'
    Foo('FOO').lower() # => 'foo'

    Foo('foo').wrong_method() # => raises AttributeError: 'str' object has no attribute 'wrong_method'

    Foo('foo').wrong_attribute() # => raises AttributeError: 'Foo' object has no attribute 'not_an_attribute'

As a shortcut you can use pass any number of methods or properties to delegate 

    @delegate('v', 'upper', 'lower')
    class Foo:
        def __init__(self, v):
            self.v = v

Example using properties instead of methods

    class Bar:
        def __init__(self):
            self._param = 0
        @property
        def param(self):
            return self._param
        @param.setter
        def param(self, param):
            self_param = param

    @delegate('v', 'param')
    class Foo2:
        def __init__(self):
            self.v = Bar()

    foo2 = Foo2()
    foo2.param  # => 0
    
    foo2.param = 2
    foo2.param  # => 2
 

# Running tests

Simply run the module `python -m delegateto`
