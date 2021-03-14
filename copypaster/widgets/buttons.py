from copypaster import log, State, AppState
from app.signal_bus import emit
import hashlib
from app.register import Register as __
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk  # noqa

MAX_LENGTH_OF_BUTTON = 20

def camel_case_split(str):
    words = [[str[0]]]

    for c in str[1:]:
        if words[-1][-1].islower() and c.isupper():
            words.append(list(c))
        else:
            words[-1].append(c)

    return ["".join(word) for word in words]

class Id:
    def hash(self):
        return hashlib.md5(repr(self.snippet).encode()).hexdigest()

    @property
    def _id(self):
        return self.hash()

class Copy(Gtk.Button, Id):

    @property
    def name(self):
        return self.snippet.name

    @name.setter
    def name(self, name):
        self.snippet.name = name

    @property
    def content(self):
        return self.snippet.content

    @content.setter
    def content(self, content):
        self.snippet.content = content

    def set_path(self, path):
        self.snippet.set_path(path)

    def save(self):
        self.snippet.save()

    def delete(self):
        self.snippet.delete()

    def __init__(self, snippet):
        self.snippet = snippet

        super(Copy, self).__init__(label=self.style_label())

        self.tag = "normal"
        

        button_context = self.get_style_context()
        button_context.add_class(self.tag)

        self.connect("clicked", self.on_copy)

    def style_label(self):
        name = self.name

        if len(name) > MAX_LENGTH_OF_BUTTON:
            name = name[:MAX_LENGTH_OF_BUTTON] + "..."

        return name

    def on_copy(self, button):
        log.debug("Handling the button press...")
        state = AppState["app"]

        if state == State.REMOVE:
            log.debug("Removing button...")
            emit("remove_button", self)

        if state in [State.NORMAL, State.AUTOSAVE]:
            log.debug("Coping value...")
            emit("copy", button.content)
            emit("preview_content", button.content)

        if state == State.EDIT:
            log.debug("Editing button...")
            emit("edit_button", self)

    def __str__(self):
        return f"<Copy [{self.name}] >"

class GoTo(Gtk.Button, Id):
    def __init__(self, name, position, destination):

        "Current position will be hidden. \
         Destination will be shown"

        self.name = name
        self.current_position = position
        self.destination = destination

        super(Gtk.Button, self).__init__(label=name)
        
        self.set_name = (
            "nested-navigation"  # TODO: styles should be moved to another class
        )

        button_context = self.get_style_context()
        button_context.add_class("nested-navigation")

        self.connect("clicked", self.on_goto)

    def __str__(self):
        return f"<GoTo [{self.name}] {self.current_position} -> {self.destination} >"

    def hash(self):
        return hashlib.md5(str(self).encode()).hexdigest()

    def on_goto(self, button: Gtk.Button):
        log.debug(f"Going to {self.destination}")
        state = AppState["app"]

        if state == State.REMOVE:
            log.debug("Removing button...")
            emit("remove_button", self)

        if state != State.REMOVE:
            emit("change_button_grid", self.current_position, self.destination)

    def delete(self):
        import os
        os.rmdir(os.path.join(self.current_position, self.name))
