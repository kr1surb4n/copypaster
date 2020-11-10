from copypaster.register import Register as __, register_instance
from copypaster import log, State, AppState
from copypaster.signal_bus import signal_bus
from copypaster.widgets.notebooks import ButtonGrid, Deck, ButtonCollection


class LoadButtonDecks:
    def start_app(self):
        """Here we load dirty notes (first) and then the rest of the
        notes.

        On event: start_app  """
        log.debug("LoadButtonDecks is run")

        cabinet = __.FileCabinet
        self.load_dirty_notes(cabinet)
        self.load_notes(cabinet)

        collections = self.load_collections(cabinet)

        cabinet.show_all()  # redraw everything

        self.set_visibility_on_collections(collections)

    def load_dirty_notes(self, cabinet):
        log.debug("Loading Dirty Notes")
        name, deck_file = __.Config.get_dirty_deck()

        dirty_notes = ButtonGrid(Deck(deck_file))

        # we need to add those objects to Register
        __.DirtyNotes = dirty_notes
        __.Dirty = dirty_notes.button_deck

        cabinet.add_page(name, dirty_notes)

    def load_notes(self, cabinet):
        """Load all notes that arent the DirtyNotes"""
        log.debug("Loading notes")

        decks = __.Config.get_decks()

        for name, deck_file in decks.items():
            cabinet.add_page(name, ButtonGrid(Deck(deck_file)))

    def load_collections(self, cabinet):
        log.debug("Loading collections")

        results = []

        collections = __.Config.get_collections()
        for name, collection_file in collections.items():
            # I build buttons collection
            collection = ButtonCollection(name, collection_file)
            results += [collection]

            # add this to the register under it's name
            setattr(__, name, collection)

            # then add this as a page
            cabinet.add_page(name, collection)

        return results

    def set_visibility_on_collections(self, collections):
        """We must hide all objects on collections and show all roots"""
        for collection in collections:
            collection.hide_all_grids()
            collection.show_root()


class OperateBranchGrids:
    def change_button_grid(self, report_to, current, target):
        log.debug(
            "Switch to the other branch from {} to  {} in {}".format(
                current, target, report_to
            )
        )
        collection = getattr(__, report_to)  # get the collection from register
        collection.current = target
        collection.grids[current].hide()
        collection.grids[target].show()


signal_bus.subscribe("start_app", LoadButtonDecks())
signal_bus.subscribe("change_button_grid", OperateBranchGrids())
