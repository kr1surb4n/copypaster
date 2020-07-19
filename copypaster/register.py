import functools

# Sachen - to rzeczy, ale
# ale jebac obce języki
class Rzeczy:
    """Here I keep the names of the things I use in the app.
    Names will be used later to make stuff nicer.
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
    When the object name is in Rzeczy, you can access it
    by using i.e. `_.Config` you will get object under the
    key `Config`.
    """

    def __setattr__(self, name, value):
        if name in self.names:
            self[name] = value
        else:
            super(ObjectRegister, self).__setattr__(name, value)

    def __getattr__(self, name):
        if name in self.names:
            return self[name]
        return super(ObjectRegister, self).__getattr__(name)


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
