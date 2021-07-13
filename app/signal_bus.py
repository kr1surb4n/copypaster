from app.register import register_instance
from app import log
import app.events as event

"""
SignalBus

is an Event Subscribe-Emit object

You need an object that implements function `<EVENT_NAME>`.
This object is subscribed by passing: <EVENT_NAME> and the object itself.
Or by using a decorator `@subscribe(<EVENT_NAME>)`

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

    def subscribe(self, event_name, callback):
        log.info(f"Subscribed {callback.__name__} for event {event_name}")
        if event_name not in self.receivers:
            self.receivers[event_name] = []

        self.receivers[event_name] += [callback]

    def emit(self, event_name, *args, **kwargs):
        log.info(f"Emited {event_name}")
        receivers = self.receivers.get(event_name, None)

        if receivers is None:
            return False

        try:
            # TODO: add async
            [callback(*args, **kwargs) for callback in receivers]
        except Exception as e:
            log.critical(str(e))
            return False

        return True

    def unsubscribe(self, event_name):
        log.info(f"Unsubscribe {event_name}")
        self.receivers[event_name] = []

signal_bus = SignalBus()

def make_subscribe(signal_bus):
    def subscriber(func):
        signal_bus.subscribe(func.__name__, func)
        return func

    return subscriber


def make_subscribe_on(signal_bus):
    def pass_the_event(event_name):
        def subscriber(func):
            signal_bus.subscribe(event_name, func)
            return func

        return subscriber

    return pass_the_event


subscribe = make_subscribe(signal_bus)
subscribe_on = make_subscribe_on(signal_bus)


def make_emit(signal_bus):
    def emiter(event, *args, **kwargs):
        return signal_bus.emit(event, *args, **kwargs)

    return emiter


emit = make_emit(signal_bus)
