import functools

Register = dict()


def register_instance(cls):
    @functools.wraps(cls)
    def wrapper_decorator(*args, **kwargs):

        instance = cls(*args, **kwargs)

        Register[cls.__name__] = instance
        return instance
    return wrapper_decorator
