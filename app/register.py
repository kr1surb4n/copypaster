"""This is dictionary object storing object used within the
application.

It is a Register of objects.

Usage:

```
# create the register
Register = ObjectRegister()

# decorate a class
@register_instance
class SomeObject:
    def __init__(self):
        self.value = 1

# create an instance
instance = SomeObject()

# you can access the instance with:
Register.SomeObject

```

Import it like this, for easier use:
```from register import Register as __```

With that in our example, you could
access the instance with:
```__.SomeObject     # way better then Register.SomeObject```


"""
import functools


class ObjectRegister(dict):
    def __setattr__(self, name, value):
        self[name] = value

    def __getattr__(self, name):
        return self[name]


Register = ObjectRegister()


def register_instance(cls):
    """This decorator adds the object instance to the Registry,
    when the decorated object is initiated.

    Registered object is accessible through it's class name.


    """

    @functools.wraps(cls)
    def wrapper_decorator(*args, **kwargs):

        instance = cls(*args, **kwargs)

        Register[cls.__name__] = instance  # hmm, this dictates the CamelCase names

        return instance

    return wrapper_decorator


def test_object_register():
    """First test to see if the ObjectRegister works"""
    dummy = "Stub"
    value = " "

    reg = ObjectRegister()

    reg[dummy] = value

    assert dummy in reg  # is dummy in register?
    assert reg.Stub  # can i access the Stub by name?
    assert reg.Stub == value  # is value correct?

    reg.Stub = 1  # can I change the value?
    assert reg.Stub == 1

    # does the setter and getter send exceptions on bad key?
    import pytest

    with pytest.raises(KeyError):
        reg.Exception


def test_decorator():
    """Next lets see if the register_instance works"""

    @register_instance
    class SomeObject:
        """Our test object"""

        def __init__(self):
            self.value = 1

    global Register

    instance = SomeObject()

    assert Register.SomeObject  # is object in Register?
    assert Register.SomeObject.value == 1  # is the value correct?

    del instance
