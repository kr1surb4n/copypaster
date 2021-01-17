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


class Signals(dict):
    def __getattr__(self, name):
        return self[name]


@register_instance
class SignalBus:
    def __init__(self):
        # super().__init__()
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
            # TODO: add async
            [callback(*args, **kwargs) for callback in receivers]
        except Exception as e:
            log.critical(str(e))
            raise e

        return True


signal_bus = SignalBus()

signals = Signals()


def make_subscribe(signals, signal_bus):
    def subscriber(func):
        signal_bus.subscribe(func.__name__, func)
        signals[func.__name__] = func.__name__

        return func

    return subscriber


subscribe = make_subscribe(signals, signal_bus)


def make_emit(signal_bus):
    def emiter(event, *args, **kwargs):
        return signal_bus.emit(event, *args, **kwargs)

    return emiter


emit = make_emit(signal_bus)


def test_signals():

    signals = Signals()
    signal_bus = SignalBus()

    subscribe = make_subscribe(signals, signal_bus)

    name = 'name'
    second_name = 'second_name'
    value = 1
    second_value = 2

    signals[name] = value
    signals[second_name] = second_value

    assert signals.name == value
    assert signals.second_name == second_value
    assert signals.name != signals.second_name

    counter = 1

    @subscribe
    def count():
        nonlocal counter
        counter += 1
        return counter

    assert counter == 1

    # subscribe works
    assert signals.count == 'count'

    # subscribe didn't run the function
    assert counter == 1  # a sanity check

    # count work
    assert count() == 2
    assert counter == 2

    assert signal_bus.emit(signals.count)
    assert counter == 3

    emit = make_emit(signal_bus)

    assert emit(signals.count)
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

    sbus = SignalBus()

    sbus.subscribe(test_event, success.test_event)
    assert sbus.emit(test_event)

    assert success.x == 1

    import pytest

    sbus.subscribe(test_event, second.test_event)
    sbus.emit(test_event)

    assert second.y == 1
    assert success.y == 2

    assert not sbus.emit(test_error)
