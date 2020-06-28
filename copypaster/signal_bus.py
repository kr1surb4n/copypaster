from copypaster.register import register_instance
from copypaster import logger
"""
SignalBus

is an Event Subscribe-Emit object

You need an object that implements function `on_<EVENT_NAME>`. 
This object is subscribed by passing: <EVENT_NAME> and the object itself. 

To emit an event you need SignalBus object and pass to emit function
an event name and arguments. Ths will call every subscribed function.



I run `emit` function and this runs some functions. I don't know what happens.
"""


@register_instance
class SignalBus:
    def __init__(self):
        # super().__init__()
        self.recievers = {}

    def subscribe(self, event_name, _object):
        callback_name = "on_" + event_name

        if not hasattr(_object, callback_name):
            raise NotImplementedError(
                "Object {} has no callback function called {}".format(_object, callback_name))

        if event_name not in self.recievers:
            self.recievers[event_name] = []

        self.recievers[event_name] += [getattr(_object, callback_name)]

    def emit(self, event_name, *args, **kwargs):
        logger.debug("Run for: " + event_name)
        receivers = self.recievers.get(event_name, None)

        if receivers is None:
            return False

        [callback(*args, **kwargs) for callback in receivers]


signal_bus = SignalBus()
