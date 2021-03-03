from copypaster import log
from app.register import register_instance
from copypaster.file_loader import DeckCollection, NavigationDeck
from app.widgets.utility import wrap
from copypaster.widgets.buttons import NavigateButton


import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk  # noqa


class ButtonGrid(Gtk.FlowBox):
    "Main area of user interface content."

    def __init__(self):
        Gtk.FlowBox.__init__(self)

        self.buttons = []

        self.set_valign(Gtk.Align.START)

        # self.set_max_children_per_line(4)
        self.set_selection_mode(Gtk.SelectionMode.NONE)

    def append(self, button):
        button.hide()
        self.add(button)
    
    def save_grid(self):# TODO: is it needed?
        pass


@register_instance
class FileCabinet(Gtk.Notebook):
    """Here we keep the buttons grids and stuff"""

    def __init__(self):
        Gtk.Notebook.__init__(self, vexpand=True)
        self.set_vexpand(True)
        self.set_resize_mode(Gtk.ResizeMode.PARENT)
        self.pages = []

    def add_page(self, title, _object):
        self.pages += [_object]
        self.append_page(wrap(_object), Gtk.Label(title))
