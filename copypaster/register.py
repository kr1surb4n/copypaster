import functools


class ObjectRegister(dict):
    def __lt__(self, other):
        name, value = other

        self[name] = value


Register = ObjectRegister()


def register_instance(cls):
    @functools.wraps(cls)
    def wrapper_decorator(*args, **kwargs):

        instance = cls(*args, **kwargs)

        Register < (cls.__name__, instance,)

        return instance
    return wrapper_decorator
