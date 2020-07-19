from copypaster.register import Register as __,  register_instance
from copypaster.signal_bus import signal_bus
from copypaster.file_loader import Deck, DeckCollection, NavigationDeck
from copypaster.widgets.utility import wrap
from copypaster.widgets.buttons import NavigateButton


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk  # noqa


class ButtonGrid(Gtk.FlowBox):
    "Main area of user interface content."

    def __init__(self, deck = None):
        Gtk.FlowBox.__init__(self)

        self.button_deck = deck

        self.set_valign(Gtk.Align.START)

        # self.set_max_children_per_line(4)
        self.set_selection_mode(Gtk.SelectionMode.NONE)

        deck is not None and self.init_buttons()

    def init_buttons(self):
        for button in self.button_deck.get_buttons():
            self.add(button)


    def save_deck(self):
        self.button_deck.save_buttons()



class ButtonCollection(Gtk.Stack):
    "Object representing whole tree walking device"


    def __init__(self, collection_name, collection_file):
        Gtk.Stack.__init__(self)

        self.name = collection_name
        self.collection = DeckCollection(collection_name, collection_file)

        # zbuduj gridsy
        self.grids = {name: ButtonGrid() for name, _ in self.collection.branches()}


        # can this I do in DeckCollection or here, where I
        # can operate on instance of a DeckCollection?
        for name, deck in self.collection.branches():
            parent_name = self.collection.parents[name]
            link_names = self.collection.levels[name]

            current = self.grids[name]

            """Fuck me, why I make so damn hard this thing??

            I should have send some stuff to somewhere that will
            open the grid for me.

            I should send a fucking message. Not do everything alone.
            """

            if name == "root": # we will build navigation deck

                current.button_deck = NavigationDeck(name,
                                    collection_name,
                                    link_names)
                current.init_buttons()
                current.hide()
                continue

            # we need to build some things into
            # branch_deck
            branch_deck = self.collection.branch_decks[name]

            # like a back button...
            branch_deck.one_up_button = NavigateButton(
                label="..",
                report_to=collection_name,
                current=name,
                target=parent_name
            )

            # or buttons to other stuff..
            branch_deck.links_buttons = [NavigateButton(# is what we will display
                        label=target_name,
                        report_to=collection_name,
                        current=name,
                        target=target_name) # we take button grid
                     for target_name in link_names]


            # then add the branch_deck to current grid object
            # and initialize buttons
            current.button_deck = branch_deck
            current.init_buttons()
            current.hide()

        # we must add all grids
        [self.add_named(grid, name) for name, grid in self.grids.items()]
        [grid.hide() for _, grid in self.grids.items()]
       
        self.grids["root"].show()
        print(self.grids.keys())

    def save_deck(self):  #TODO make stuff for this to work
        self.button_deck.save_buttons()

    def hide_all_grids(self):
        [grid.hide() for _, grid in self.grids.items()]

    def show_root(self):
        # lets show the first button_grid
        self.grids["root"].show()


@register_instance
class FileCabinet(Gtk.Notebook):
    """Here we keep the buttons grids and stuff"""

    def __init__(self):
        Gtk.Notebook.__init__(self, vexpand=True)
        self.pages = []

    def add_page(self, title, _object):
        self.pages += [_object]
        self.append_page(wrap(_object), Gtk.Label(title))
