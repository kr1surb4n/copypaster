"""
ButtonGrid is FlowBox keeping Buttons
ButtonTree is a Stack that is keeping all the tree (its a tree, the tree)

Collections are keept as dictionaries:
{
    'path/to/collection/folder': ButtonGrid([ Buttons..... ]),
    'path/to/collection/folder/category1': ButtonGrid([ Buttons..... ])
    'path/to/collection/folder/category1/categoryA': ButtonGrid([ Buttons..... ])
    'path/to/collection/folder/category2': ButtonGrid([ Buttons..... ])
    'path/to/collection/folder/category2/unicorn': ButtonGrid([ Buttons..... ])
    'path/to/collection/folder/category2/cow/pigglets': ButtonGrid([ Buttons..... ])
    'path/to/collection/folder/category3': ButtonGrid([ Buttons..... ])
    ...
}

In folder are buttons to category1, category2, category3...
In category1 is a button that leads to categoryA.
In category2 is a button that leads to unicor.
In cow is a button that leads to pigglets.
....
you get the idea. And in "folder" you can have normal buttons.
do what you want.

"""

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk  # noqa

from copypaster import log


class ButtonGrid(Gtk.FlowBox):
    """As the name says. Generally it's a wrapper on a list
    that is displayed as a grid of buttons"""

    def __init__(self, buttons={}):
        Gtk.FlowBox.__init__(self)

        self.buttons = buttons

        self.set_valign(Gtk.Align.START)
        self.set_selection_mode(Gtk.SelectionMode.NONE)

    def append(self, button):
        log.debug(f"Adding button: {button}")
        self.buttons[button._id] = button
        self.add(button)

    def remove(self, button):
        del self.buttons[button._id]
        super().remove(button)

class ButtonTree(Gtk.Stack):
    "Object representing whole tree of folders and files"

    @property
    def current_grid(self):
        return self.tree[self.current_position]

    def __init__(self):
        Gtk.Stack.__init__(self)
        self.level = ""
        self.current = None
        self.tree = {}

    def initialize(self, tree: dict, root: str):
        log.debug(f"Initializing snippets folder: {root}")
        self.tree = tree
        self.root = root
        self.level = root

        for name, grid in self.tree.items():
            self.add_named(grid, name)

    def goto(self, destination):
        self.current_position = destination
        self.set_visible_child_name(destination)

    def add_to_current_grid(self, button):
        self.current_grid.append(button)

    def remove_button_from_current_grid(self, button):
        self.current_grid.remove(button)

    def show_root(self):
        log.debug("Back to root")
        self.set_visible_child_name(self.root)
