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


def make_register_instance(Register):
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

    return register_instance


register_instance = make_register_instance(Register)


def test_object_register():
    """Test if the ObjectRegister works.

    Basic tests.
    """
    Thing = "Thing"
    value = " "

    Register = ObjectRegister()

    Register[Thing] = value

    assert Thing in Register

    # is the Thing like a property?
    assert Register.Thing

    # is the value of the Thing ok?
    assert Register.Thing == value

    # can I change the value?
    Register.Thing = 1
    assert Register.Thing == 1
    assert Register.Thing != value

    # is getter sending exceptions when asked for a wrong object?
    import pytest

    with pytest.raises(KeyError):
        Register.IDontExist


def test_register_instance():
    """is the register_instance working?"""

    Register = ObjectRegister()
    register_instance = make_register_instance(Register)

    @register_instance
    class SomeObject:
        """Our test object"""

        def __init__(self):
            self.value = 1

    instance = SomeObject()

    assert Register.SomeObject
    assert Register.SomeObject == instance
    assert Register.SomeObject.value == 1

    del instance
