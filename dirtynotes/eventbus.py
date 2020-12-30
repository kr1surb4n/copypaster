# import gi
# gi.require_version("Gtk", "3.0")
# from gi.repository import Gtk

# window = Gtk.Window(title="Hello World")
# window.show()
# window.connect("destroy", Gtk.main_quit)
# Gtk.main()


class SignalBus:
    def __init__(self):
        # super().__init__()
        self.recievers = {}

    def subscribe(self, event_name, _object):
        callback_name = "on_" + event_name

        if not hasattr(_object, callback_name):
            raise NotImplementedError(
                "Object {} has no callback function called {}".format(
                    _object, callback_name
                )
            )

        if event_name not in self.recievers:
            self.recievers[event_name] = []

        self.recievers[event_name] += [getattr(_object, callback_name)]

    def emit(self, event_name, *args, **kwargs):
        receivers = self.recievers.get(event_name, None)

        if receivers is None:
            return False

        [callback(*args, **kwargs) for callback in receivers]


ebus = EventBus()

# objectA  has   on_event_name


class ObjectA:
    def on_event_name(self, arg1):
        print("event was run " + arg1)


objectA = ObjectA()
objectA2 = ObjectA()
# objectA  subscribes to EventBus for event_name

ebus.subscribe("event_name", objectA)
ebus.subscribe("event_name", objectA2)

# objectB  emits  an    event_name   using   EventBus


ebus.emit("event_name", "and some data was send")
ebus.emit("event_name", "- another")
