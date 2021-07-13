import pytest
from app.signal_bus import SignalBus, make_subscribe, make_emit

def test_signals():
    signal_bus = SignalBus()

    subscribe = make_subscribe(signal_bus)
    emit = make_emit(signal_bus)

    signal_name = 'count'
    counter = 1

    # sanity checks
    assert counter == 1
    assert len(signal_bus.receivers.items()) == 0
    assert signal_bus.emit(signal_bus) == False

    @subscribe
    def count():
        nonlocal counter
        counter += 1
        return counter

    # is function subscribed?
    assert len(signal_bus.receivers.items()) == 1
    assert len(signal_bus.receivers[signal_name]) == 1

    # count workS
    assert count() == 2
    assert counter == 2

    # emit signal
    assert signal_bus.emit(signal_name)
    assert counter == 3 

    # test emit function
    assert emit(signal_name)
    assert counter == 4

    @subscribe
    def fails():
        return 1/0

    assert False == emit('fails')

def test_signal_bus():
    """Here I test the signal bus"""

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
