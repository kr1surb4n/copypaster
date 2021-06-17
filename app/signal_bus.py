from app.register import register_instance
from app import log
import functools

"""
SignalBus

is an Event Subscribe-Emit object

You need an object that implements function `on_<EVENT_NAME>`.
This object is subscribed by passing: <EVENT_NAME> and the object itself.

To emit an event you need SignalBus object and pass to emit function
an event name and arguments. Ths will call every subscribed function.

I run `emit` function and this runs some functions. I don't know what happens."""


def not_implemented(event_name):
    def wrapps(*args, **kwargs):
        raise NotImplementedError("something has not implemented " + event_name)

    return wrapps


@register_instance
class SignalBus:
    def __init__(self):
        self.receivers = {}

    def unsubscribe(self, event_name):
        if event_name in self.receivers:
            del self.receivers[event_name]

    def subscribe(self, event_name, callback):
        if event_name not in self.receivers:
            self.receivers[event_name] = []

        self.receivers[event_name] += [callback]

    def emit(self, event_name, *args, **kwargs):

        log.debug("Run for: " + event_name)
        receivers = self.receivers.get(event_name, None)

        if receivers is None:
            return False

        try:
            # TODO: maybe add async
            [callback(*args, **kwargs) for callback in receivers]
        except Exception as e:
            log.critical(str(e))
        return True


signal_bus = SignalBus()


def make_subscribe(signal_bus):
    def subscriber(func):
        signal_bus.subscribe(func.__name__, func)

        return func

    return subscriber


subscribe = make_subscribe(signal_bus)


def make_emit(signal_bus):
    def emiter(event, *args, **kwargs):
        return signal_bus.emit(event, *args, **kwargs)

    return emiter


emit = make_emit(signal_bus)


def test_signals():
    signal_bus = SignalBus()

    subscribe = make_subscribe(signal_bus)

    counter = 1

    @subscribe
    def count():
        nonlocal counter
        counter += 1
        return counter

    signal_name = count.__name__

    # subscribe didn't run the function
    assert counter == 1  # a sanity check

    # count workS
    assert count() == 2
    assert counter == 2

    # emit signal
    assert signal_bus.emit(signal_name)
    assert counter == 3

    emit = make_emit(signal_bus)

    # test emit function
    assert emit(signal_name)
    assert counter == 4


def test_signal_bus():
    """Here I test the signall buss"""

    # event names
    test_event = "test_event"
    test_error = "test_error"

    class Simplex:
        """is used as an example object,
        that demonstrates that stuff works"""

        y = 0

        def __init__(self):
            self.x = 0

        def test_event(self):
            self.x += 1
            self.y += 1

    success = Simplex()
    second = Simplex()

    signal_bus = SignalBus()

    signal_bus.subscribe(test_event, success.test_event)
    assert signal_bus.emit(test_event)

    assert success.x == 1

    signal_bus.subscribe(test_event, second.test_event)
    signal_bus.emit(test_event)

    assert second.y == 1
    assert success.y == 2

    assert not signal_bus.emit(test_error)
