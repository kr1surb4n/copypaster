from app.register import Register as __
from copypaster import log
from app.signal_bus import emit, subscribe
from copypaster.file_loader import Deck
from copypaster.widgets.notebooks import ButtonGrid, ButtonCollection


@subscribe
def start_app():
    load_config()

@subscribe
def quit():
    log.debug("Quitting...")

def load_config():
    """Here we load dirty notes (first) and then the rest of the
    notes.

    On event: start_app"""
    log.debug("LoadButtonDecks is run")

    cabinet = __.FileCabinet
    load_dirty_notes(cabinet)
    load_notes(cabinet)

    collections = load_collections(cabinet)

    __.main_window.show_all()  # redraw everything

    set_visibility_on_collections(collections)


def load_dirty_notes(cabinet):
    log.debug("Loading Dirty Notes")
    name, deck_file = __.Config.get_dirty_deck()

    dirty_notes = ButtonGrid(Deck(deck_file))

    # we need to add those objects to Register
    __.DirtyNotes = dirty_notes
    __.Dirty = dirty_notes.button_deck

    cabinet.add_page(name, dirty_notes)


def load_notes(cabinet):
    """Load all notes that arent the DirtyNotes"""
    log.debug("Loading notes")

    decks = __.Config.get_decks()

    for name, deck_file in decks.items():
        cabinet.add_page(name, ButtonGrid(Deck(deck_file)))


def load_collections(cabinet):
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


def set_visibility_on_collections(collections):
    """We must hide all objects on collections and show all roots"""
    for collection in collections:
        collection.hide_all_grids()
        collection.show_root()

@subscribe
def change_button_grid(report_to, current, target):

    log.debug(
        "Switch to the other branch from {} to  {} in {}".format(
            current, target, report_to
        )
    )
    collection = getattr(__, report_to)  # get the collection from register
    collection.current = target

    # The whole secret to navigation is that nothing moves.
    # All is static, we only show and hide stuff"
    collection.grids[current].hide()
    collection.grids[target].show()
