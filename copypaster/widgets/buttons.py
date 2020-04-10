from copypaster import logger, State, NORMAL, AUTOSAVE, REMOVE, EDIT
import time
import sys
import gettext
import datetime
import hashlib
from copypaster.register import Register, register_instance
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio  # noqa


class CopyButton(Gtk.Button):

    def hash(self):
        val = self.name + self.value
        return hashlib.md5(val.encode()).hexdigest()

    def serialize(self):
        return {'name': self.name, 'value': self.value}

    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name', None)
        self.value = kwargs.get('value', None)

        assert self.value is not None, "There is no value for {}".format(
            self.name)

        self.value = str(self.value)
        del kwargs['value']

        if not self.name:
            self.name = str(self.value)
        else:
            del kwargs['name']

        self.id = self.hash()

        kwargs['label'] = self.name
        super(CopyButton, self).__init__(*args, **kwargs)

        self.connect('clicked', self.on_button_click)

    def on_button_click(self, button):
        logger.debug(
            "Clicked button: {} and copied value".format(button.value))

        state = State['app']

        if state == REMOVE:
            del self.get_parent().get_parent().button_deck.buttons[self.value]
            self.get_parent().remove(self)

        if state in [NORMAL, AUTOSAVE]:
            Register['Jimmy'].send(button.value)
            Register['StatusBar'].send(
                'Clicked button number %s' % button.value)

        if state == EDIT:
            Register['NewNote'].edit(**self.serialize())


class PasteButton(Gtk.Button):

    def __init__(self, *args, **kwargs):
        kwargs['label'] = "Save from Clip"
        super(PasteButton, self).__init__(*args, **kwargs)

        self.connect('clicked', self.on_button_click)

    def on_button_click(self, button):
        logger.debug(
            "Clicked button: {} and copied value".format(button.value))

        contents = Register['Jimmy'].recieve()
        if contents:
            Register['Jimmy'].send(button.value)
            Register['StatusBar'].send(
                'Clicked button number %s' % button.value)
