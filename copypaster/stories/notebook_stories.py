from copypaster.register import Register as __
from copypaster import logger
from copypaster.signal_bus import signal_bus


class NotebookStories:
    def on_new_notebook(self):
        pass

    def on_open_notebook(self):
        pass

    def on_save_notebook(self):
        # TODO: move this to FileCabinet
        cabinet = __['FileCabinet']
        cabinet.pages[cabinet.get_current_page()].save_deck()

    def on_save_notebook_as(self):
        dialog = Gtk.FileChooserDialog(         # TODO: move this to FileCabinet
            'Save button deck', self.win,
            Gtk.FileChooserAction.SAVE,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        dialog.set_do_overwrite_confirmation(True)
        if dialog.run() == Gtk.ResponseType.OK:
            filename = dialog.get_filename()

            cabinet = __['FileCabinet']
            current_deck = cabinet.pages[cabinet.get_current_page()]

            try:
                current_deck.button_deck.path = filename
                current_deck.button_deck.save_buttons()
            except Exception as e:
                logger.error("There was an exception {}".format(e))
        dialog.destroy()

    def on_start_app(self):
        """Here we load dirty notes (first) and then the rest of the
        notes.

        On event: start_app
        """
        logger.debug("LoadButtonDecks is run")

        cabinet = __['FileCabinet']
        self.load_dirty_notes(cabinet)
        self.load_notes(cabinet)
        self.load_collections(cabinet)

        cabinet.show_all()  # redraw everything

    def load_dirty_notes(self, cabinet):
        logger.debug('Loading Dirty Notes')
        name, deck_file = __['Config'].get_dirty_deck()

        dirty_notes = ButtonGrid(deck_file)

        # we need to add those objects to Register
        __['DirtyNotes'] = dirty_notes
        __['Dirty'] = dirty_notes.button_deck

        cabinet.add_page(name, dirty_notes)


signal_bus.subscribe('new_notebook', LoadButtonDecks())
signal_bus.subscribe('open_notebook', LoadButtonDecks())
signal_bus.subscribe('save_notebook', LoadButtonDecks())
signal_bus.subscribe('save_notebook_AS', LoadButtonDecks())
