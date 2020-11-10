from copypaster.register import Register as __
from copypaster import log
from copypaster.signal_bus import signal_bus


class NotebookStories:
    def new_notebook(self):
        pass

    def open_notebook(self):
        pass

    def save_notebook(self):
        # TODO: move this to FileCabinet
        cabinet = __.FileCabinet
        cabinet.pages[cabinet.get_current_page()].save_grid()

    def save_notebook_as(self):
        pass
        """
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
                log.error("There was an exception {}".format(e))
        dialog.destroy()
        """


notebook_stories = NotebookStories()

# stories:
new_notebook = "new_notebook"
open_notebook = "open_notebook"
save_notebook = "save_notebook"
save_notebook_as = "save_notebook_as"

signal_bus.register(
    notebook_stories, new_notebook, open_notebook, save_notebook, save_notebook_as
)
