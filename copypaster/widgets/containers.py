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

from copypaster.widgets.buttons import Copy, GoTo, AddFolder, AddSnippet, FunctionalButton
from copypaster import log

def copy_is_before_goto(first, second):
    return isinstance(first, Copy) and isinstance(second, GoTo)

def goto_is_before_copy(first, second):
    return isinstance(first, GoTo) and isinstance(second, Copy)

def left_is_functional(left, right):
    return isinstance(left, FunctionalButton)

def right_is_function(left, right):
    return isinstance(right, FunctionalButton)

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

def function_button_last(first, second):
    if right_is_function(first, second):
        return FIRST_STAYS_FIRST
    if left_is_functional(first, second):
        return FIRST_GOES_SECOND

def sort_by_order(first, second):
    if first.order < second.order:
        return FIRST_STAYS_FIRST
    if first.order > second.order:
        return FIRST_GOES_SECOND
    return NOTHING_CHANGES

how_to_sort = {
    ("Copy", "Copy"): sort_by_content,
    ("GoTo", "GoTo"): sort_by_name,
    ("Copy", "GoTo"): sort_by_type,
    ("GoTo", "Copy"): sort_by_type,

    ("GoTo", "AddS"): function_button_last,
    ("AddS", "GoTo"): function_button_last,
    ("GoTo", "AddF"): function_button_last,
    ("AddF", "GoTo"): function_button_last,

    ("Copy", "AddS"): function_button_last,
    ("AddS", "Copy"): function_button_last,
    ("Copy", "AddF"): function_button_last,
    ("AddF", "Copy"): function_button_last,

    ("AddF", "AddS"): sort_by_order,
    ("AddS", "AddF"): sort_by_order,
    ("AddS", "AddS"): sort_by_order,
    ("AddF", "AddF"): sort_by_order,
}

ex = lambda x: str(x)[1:5]

def sort_function(child1: Gtk.FlowBoxChild, child2: Gtk.FlowBoxChild, *user_data):
    first = child1.get_children()[0]
    second = child2.get_children()[0]

    sort = how_to_sort[(ex(first), ex(second))]
    return sort(first, second)


class ObjectExistsInGridException(Exception):
    ...
    
class ButtonGrid(Gtk.FlowBox):
    """As the name says. Generally it's a wrapper on a list
    that is displayed as a grid of buttons"""

    def __init__(self, buttons={}, path: str = None, parent_path: str = None):
        Gtk.FlowBox.__init__(self)

        self.buttons = buttons

        self.set_valign(Gtk.Align.START)
        self.set_selection_mode(Gtk.SelectionMode.NONE)
        self.set_sort_func(sort_function)

        snippet = AddSnippet()
        self.append(snippet)
        snippet.show()

        folder = AddFolder()
        self.append(folder)
        folder.show()

    def append(self, button):
        log.debug(f"Adding button: {button}")

        if button._id in self.buttons:
            raise ObjectExistsInGridException(str(button))

        self.buttons[button._id] = button
        self.add(button)

    def remove(self, button):
        super().remove(button)
        button.delete()
        del self.buttons[button._id]
        

    def add_go_to_parent_button(self, current, parent):
        up_to_parent = GoTo(
                    name="..",
                    position=current,
                    destination=parent
        )
        up_to_parent.show()
        self.append(up_to_parent)

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

        button.set_path(self.current_level)
        button.save()
        
        self.current_grid.append(button)

    def remove_button_from_current_grid(self, button):
        self.current_grid.remove(button)

    def show_root(self):
        log.debug("Back to root")
        self.set_visible_child_name(self.root)
