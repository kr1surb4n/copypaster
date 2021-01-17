import functools


class ObjectRegister(dict):
    """Is a dictionary and stores stuff. Mainly objects.
    This way you can build a complex application using very easy code.

    Below you have two functions that allow for a fancy object
    handling.
    When the object name you can access it
    by using i.e. `_.Config` you will get object under the
    key `Config`.
    """

    def __setattr__(self, name, value):
        self[name] = value

    def __getattr__(self, name):
        return self[name]

    def __lt__(self, other):
        """This function allows for fancy object assigment.
        Where `other` is a tuple: class name, instance.

        i.e.:  Register < (class.name, instance)
        """
        name, value = other

        self[name] = value


Register = ObjectRegister()

def make_register(Register):
    def registrar(object):
        Register[object.__name__] = object
        return object
    return registrar

register = make_register(Register)

def register_instance(cls):
    """This decorator adds an object instance when the object
    is initiated."""

    @functools.wraps(cls)
    def wrapper_decorator(*args, **kwargs):

        instance = cls(*args, **kwargs)

        Register[cls.__name__] = instance

        return instance

    return wrapper_decorator


def test_object_register():
    """First test to see if the ObjectRegister works"""
    dummy = "Stub"
    value = " "

    o_reg = ObjectRegister()

    o_reg[dummy] = value

    assert dummy in o_reg  # is dummy in register?

    assert o_reg.Stub == value  # is value correct?

    o_reg.Stub = 1  # can I change the value?
    assert o_reg.Stub == 1

    # does the setter and getter send exceptions on bad key?
    import pytest

    with pytest.raises(KeyError):
        o_reg.Exception

    register = make_register(o_reg)

    @register
    def number(i):
        return i

    assert o_reg.number(2) == 2

def test_decorator():
    """Next lets see if the register_instance works"""

    @register_instance
    class Manequin:
        """Our test object"""

        def __init__(self):
            self.value = 1

    global Register

    korper = Manequin()

    assert Register.Manequin  # is object in Register?
    assert Register.Manequin.value == 1  # is it's value correct?

    del korper
