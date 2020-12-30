from folders import log, State, AppState
from folders.signal_bus import signal_bus
import hashlib
from folders.register import Register as __
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk  # noqa


def camel_case_split(str):
    words = [[str[0]]]

    for c in str[1:]:
        if words[-1][-1].islower() and c.isupper():
            words.append(list(c))
        else:
            words[-1].append(c)

    return ["".join(word) for word in words]


class CopyButton(Gtk.Button):
    def hash(self):
        val = self.name + self.value
        return hashlib.md5(val.encode()).hexdigest()

    def serialize(self):
        return {
            "name": self.name,
            "value": self.value,
            "click_count": self.click_count,
            "info": self.tooltip_text,
        }

    def __init__(self, *args, **kwargs):
        self.name = kwargs.get("name", None)
        self.value = kwargs.get("value", None)
        self.click_count = kwargs.get("click_count", 0)
        self.tooltip_text = kwargs.get("info", "")
        self.tag = kwargs.get("tag", "normal")

        if "tag" in kwargs:
            del kwargs["tag"]

        assert self.value is not None, "There is no value for {}".format(self.name)

        self.value = str(self.value)
        del kwargs["value"]

        if "click_count" in kwargs:  # TODO WHats that ?
            del kwargs["click_count"]

        if "info" in kwargs:
            del kwargs["info"]

        if not self.name:
            self.name = str(self.value)
            self.name = " ".join(camel_case_split(self.name))
            self.name = self.name.strip()
        else:
            del kwargs["name"]

        self.id = self.hash()

        kwargs["label"] = self.style_label()
        super(CopyButton, self).__init__(*args, **kwargs)

        button_context = self.get_style_context()
        button_context.add_class(self.tag)

        # set the name of the thing
        self.set_tooltip_text(self.name)

        self.connect("clicked", self.on_button_click)

    def style_label(self):
        name = self.name

        MAX_LENGTH_OF_BUTTON = 20

        if len(name) > MAX_LENGTH_OF_BUTTON:
            name = name[:MAX_LENGTH_OF_BUTTON] + "..."

        return name

    def on_button_click(self, button):
        log.debug("Handling the button press...")
        state = AppState["app"]

        if state == State.REMOVE:
            log.debug("Removing button...")
            signal_bus.emit("remove_button", self)

        if state in [State.NORMAL, State.AUTOSAVE]:
            log.debug("Coping value...")
            self.click_count += 1
            signal_bus.emit("copy", button.value)

        if state == State.EDIT:
            log.debug("Editing button...")
            signal_bus.emit("edit_button", self)


class NavigateButton(Gtk.Button):
    def __init__(self, *args, **kwargs):

        "Current will be hidden. \
         Target will be shown"

        "Invoke: NavigateButton(current=<widget>, target=<widget>, label='Back')"
        self.report_to = kwargs.get("report_to")
        self.current = kwargs.get("current")
        self.target = kwargs.get("target")
        del kwargs["report_to"]
        del kwargs["current"]
        del kwargs["target"]

        super(NavigateButton, self).__init__(*args, **kwargs)
        self.set_name = (
            "nested-navigation"  # TODO: styles should be moved to another class
        )
        button_context = self.get_style_context()
        button_context.add_class("nested-navigation")

        self.connect("clicked", self.on_button_click)

    def on_button_click(self, button):
        log.debug("Navigating...")

        "The whole secret to navigation is that nothing moves. \
        All is static, but we show and hide stuff"

        signal_bus.emit("change_button_grid", self.report_to, self.current, self.target)

        # DO THAT IN THE EVENT CONTROL
        # self.current.hide()
        # self.target.show()


class PasteButton(Gtk.Button):
    def __init__(self, *args, **kwargs):
        kwargs["label"] = "Save from Clip"
        super(PasteButton, self).__init__(*args, **kwargs)

        self.connect("clicked", self.on_button_click)

    def on_button_click(self, button):
        log.debug("Clicked button: {} and copied value".format(button.value))

        contents = __.Jimmy.receive()
        if contents:
            __.Jimmy.send(button.value)
