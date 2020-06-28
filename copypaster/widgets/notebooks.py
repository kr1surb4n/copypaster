from copypaster.register import Register as __,  register_instance
from copypaster.signal_bus import signal_bus
from copypaster.file_loader import Deck
from copypaster.widgets.utility import wrap


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk  # noqa


class ButtonGrid(Gtk.FlowBox):
    "Main area of user interface content."

    def __init__(self, deck_file):
        Gtk.FlowBox.__init__(self)

        self.button_deck = Deck(deck_file)

        self.set_valign(Gtk.Align.START)
        # self.set_max_children_per_line(4)
        self.set_selection_mode(Gtk.SelectionMode.NONE)

        for button in self.button_deck.get_buttons():
            self.add(button)

    def save_deck(self):
        self.button_deck.save_buttons()


@register_instance
class FileCabinet(Gtk.Notebook):
    """Here we keep the buttons grids and stuff"""

    def __init__(self):
        Gtk.Notebook.__init__(self, vexpand=True)
        self.pages = []

    def add_page(self, title, _object):
        self.pages += [_object]
        self.append_page(wrap(_object), Gtk.Label(title))
