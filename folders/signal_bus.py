from folders.register import register_instance
from folders import log

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


class Signal:
    edit_button = "edit_button"
    copy = "copy"
    remove_button = "remove_button"


@register_instance
class SignalBus:
    def __init__(self):
        # super().__init__()
        self.receivers = {}

    def register(self, _object, *events):
        """Helper function to register whole object with all
        the events"""
        for event in events:
            self.subscribe(event, _object)

    def subscribe(self, event_name, _object):
        if event_name not in self.receivers:
            self.receivers[event_name] = []

        self.receivers[event_name] += [
            getattr(_object, event_name, not_implemented(event_name))
        ]

    def emit(self, event_name, *args, **kwargs):

        log.debug("Run for: " + event_name)
        receivers = self.receivers.get(event_name, None)

        if receivers is None:
            return False

        [callback(*args, **kwargs) for callback in receivers]


signal_bus = SignalBus()


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

    sbus.subscribe(test_event, success)
    sbus.emit(test_event)

    assert success.x == 1

    import pytest

    with pytest.raises(NotImplementedError):
        sbus.subscribe(test_error, success)

    sbus.subscribe(test_event, second)
    sbus.emit(test_event)

    assert second.y == 1
    assert success.y == 2

    assert not sbus.emit(test_error)
