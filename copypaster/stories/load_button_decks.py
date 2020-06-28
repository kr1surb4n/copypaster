from copypaster.register import Register as __, register_instance
from copypaster import logger, State, AppState
from copypaster.signal_bus import signal_bus
from copypaster.widgets.notebooks import ButtonGrid


class LoadButtonDecks:
    def on_start_app(self):
        """Here we load dirty notes (first) and then the rest of the
        notes.

        On event: start_app
        """
        logger.debug("LoadButtonDecks is run")

        cabinet = __['FileCabinet']
        self.load_dirty_notes(cabinet)
        self.load_notes(cabinet)

        cabinet.show_all()  # redraw everything

    def load_dirty_notes(self, cabinet):
        logger.debug('Loading Dirty Notes')
        name, deck_file = __['Config'].get_dirty_deck()

        dirty_notes = ButtonGrid(deck_file)

        # we need to add those objects to Register
        __['DirtyNotes'] = dirty_notes
        __['Dirty'] = dirty_notes.button_deck

        cabinet.add_page(name, dirty_notes)

    def load_notes(self, cabinet):
        """Load all notes that arent the DirtyNotes"""
        logger.debug('Loading notes')

        decks = __['Config'].get_decks()

        for name, deck_file in decks.items():
            cabinet.add_page(name, ButtonGrid(deck_file))


signal_bus.subscribe('start_app', LoadButtonDecks())
