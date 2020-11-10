from copypaster.widgets.utility import wrap
from copypaster import log, CURRENT_DIR

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Gio  # noqa


class DialogError(Gtk.Dialog):

    def __init__(self, parent, massage):  # lol
        log.debug('Ups, an error...')
        Gtk.Dialog.__init__(self)
        self.set_modal(True)
        self.add_button(button_text="OK", response_id=Gtk.ResponseType.OK)
        self.set_transient_for(parent)
        self.set_default_size(150, 100)

        label = Gtk.Label(massage)

        box = self.get_content_area()
        box.add(label)
        self.show_all()
