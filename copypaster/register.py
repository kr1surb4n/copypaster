import functools

# Sachen - to rzeczy, ale
# ale jebac obce języki
class Rzeczy:
    """Here I keep the names of the things I use in the app.
    Names will be used later to make stuff nicer.

    Update 1.08.20: from tooday this is just a list of names
    """
    names = [
        'SignalBus',
        'Config',
        'Jimmy',
        'StateButtons',
        'FileCabinet',
        'Application',
        'MainWindow',
        'DirtyNotes',
        'Dirty',
    ]


class ObjectRegister(dict, Rzeczy):
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

def register_instance(cls):
    """This decorator adds an object instance when the object
    is initiated."""
    @functools.wraps(cls)
    def wrapper_decorator(*args, **kwargs):

        instance = cls(*args, **kwargs)

        Register < (cls.__name__, instance)

        return instance
    return wrapper_decorator


def test_object_register():
    """First test to see if the ObjectRegister works"""
    dummy = 'Stub'
    value = " "

    o_reg = ObjectRegister()

    o_reg < (dummy, value)

    assert dummy in o_reg  # is dummy in register?

    assert o_reg.Stub == value  # is value correct?

    o_reg.Stub = 1              # can I change the value?
    assert o_reg.Stub == 1


    # does the setter and getter send exceptions on bad key?
    import pytest
    with pytest.raises(KeyError):
        o_reg.Exception

def test_decorator():
    """Next lets see if the register_instance works"""

    @register_instance
    class Manequin:
        """Our test object"""
        def __init__(self):
            self.value = 1


    global Register

    korper = Manequin()

    assert Register.Manequin             # is object in Register?
    assert Register.Manequin.value == 1  # is it's value correct?
