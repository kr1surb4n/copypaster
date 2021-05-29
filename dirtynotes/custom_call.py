


def emit(name, *args, **kwargs):
    print(f"Emiting {name}")
    print(name, args, kwargs)

class Parent:
    def ryba(self):
        print("ryba")


class Proxy(Parent):
    def __getattr__(self, name):
        print(f"Want to call {name}")
        try:
            return super().__getattr__(self, name)
        except AttributeError:
            ...

        print("I use method")
        def method(*args, **kwargs):
            emit(name, *args, **kwargs)
        return method

p = Proxy()

p.dupa()
p.kura(1, 2, ogon=2)
p.ryba()