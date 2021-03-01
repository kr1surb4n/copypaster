from app.register import Register as __
from app.signal_bus import subscribe


@subscribe
def new_notebook():
    pass


@subscribe
def open_notebook():
    pass


@subscribe
def save_notebook():
    # TODO: move this to FileCabinet
    # this is bollocks
    #
    # notebook is the whole config
    #
    # current page is the deck.
    cabinet = __.FileCabinet
    cabinet.pages[cabinet.get_current_page()].save_grid()


@subscribe
def save_notebook_as():
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
    pass