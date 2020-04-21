from copypaster.register import register_instance


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
        receivers = self.recievers.get(event_name, None)

        if receivers is None:
            return False

        [callback(*args, **kwargs) for callback in receivers]


signal_bus = SignalBus()
