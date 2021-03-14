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

from copypaster.widgets.buttons import Copy, GoTo
from copypaster import log

def copy_is_before_goto(first, second):
    return isinstance(first, Copy) and isinstance(second, GoTo)

def goto_is_before_copy(first, second):
    return isinstance(first, GoTo) and isinstance(second, Copy)

NOTHING_CHANGES=0

FIRST_GOES_SECOND=1
FIRST_STAYS_FIRST=-1

COPY_GOES_SECOND=1
GOTO_STAYS_FIRST=-1

def sort_by_name(first, second):
    if first.name < second.name:
        return FIRST_STAYS_FIRST
    if first.name > second.name:
        return FIRST_GOES_SECOND
    return NOTHING_CHANGES

def sort_by_content(first, second):
    if len(first.content) < len(second.content):
        return FIRST_STAYS_FIRST
    if len(first.content) > len(second.content):
        return FIRST_GOES_SECOND
    
    return sort_by_name(first, second)

def sort_by_type(first, second):
    if copy_is_before_goto(first, second):
        return COPY_GOES_SECOND
    if goto_is_before_copy(first, second):
        return GOTO_STAYS_FIRST
    return NOTHING_CHANGES

how_to_sort = {
    ("Copy", "Copy"): sort_by_content,
    ("GoTo", "GoTo"): sort_by_name,
    ("Copy", "GoTo"): sort_by_type,
    ("GoTo", "Copy"): sort_by_type,
}

ex = lambda x: str(x)[1:5]

def sort_function(child1: Gtk.FlowBoxChild, child2: Gtk.FlowBoxChild, *user_data):
    first = child1.get_children()[0]
    second = child2.get_children()[0]

    sort = how_to_sort[(ex(first), ex(second))]
    return sort(first, second)

    
class ButtonGrid(Gtk.FlowBox):
    """As the name says. Generally it's a wrapper on a list
    that is displayed as a grid of buttons"""

    def __init__(self, buttons={}):
        Gtk.FlowBox.__init__(self)

        self.buttons = buttons

        self.set_valign(Gtk.Align.START)
        self.set_selection_mode(Gtk.SelectionMode.NONE)
        self.set_sort_func(sort_function)

    def append(self, button):
        log.debug(f"Adding button: {button}")
        self.buttons[button._id] = button
        self.add(button)

    def remove(self, button):
        button.delete()
        super().remove(button)
        del self.buttons[button._id]
        

class ButtonTree(Gtk.Stack):
    "Object representing whole tree of folders and files"

    @property
    def current_grid(self):
        return self.tree[self.current_level]

    def __init__(self):
        Gtk.Stack.__init__(self)
        self.current_level = "" 
        self.tree = {}
        self.root = ""

    def initialize(self, tree: dict, root: str):
        log.debug(f"Initializing snippets folder: {root}")
        self.tree = tree
        self.root = root
        self.current_level = root

        for name, grid in self.tree.items():
            self.add_named(grid, name)

    def goto(self, destination):
        self.current_level = destination
        self.set_visible_child_name(destination)

    def add_to_current_grid(self, button):
        self.current_grid.append(button)

    def remove_button_from_current_grid(self, button):
        self.current_grid.remove(button)

    def show_root(self):
        log.debug("Back to root")
        self.set_visible_child_name(self.root)
