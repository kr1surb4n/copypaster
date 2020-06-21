from copypaster.register import Register as __, register_instance
from copypaster import logger, CURRENT_DIR, State, NORMAL, AUTOSAVE, EDIT,  REMOVE
from copypaster.file_loader import Deck
from copypaster.widgets.utility import wrap
from copypaster.widgets.dialogs import DialogError, DialogEdit


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Gio, GObject  # noqa


class ButtonGrid(Gtk.FlowBox):
    "Main area of user interface content."

    def __init__(self, deck_file):
        Gtk.FlowBox.__init__(self)

        self.button_deck = Deck(deck_file)

        self.set_valign(Gtk.Align.START)
        # self.set_max_children_per_line(4)
        self.set_selection_mode(Gtk.SelectionMode.NONE)

        for button in self.button_deck.get_buttons():
            self.add(button)

    def save_deck(self):
        self.button_deck.save_buttons()


@register_instance
class FileCabinet(Gtk.Notebook):
    """Here we keep the buttons grids and stuff"""

    def __init__(self):
        Gtk.Notebook.__init__(self, vexpand=True)
        self.pages = []

        self.load_dirty_notes()
        self.load_notes()

    def load_dirty_notes(self):
        name, deck_file = __['Config'].get_dirty_deck()

        dirty_notes = ButtonGrid(deck_file)

        __['DirtyNotes'] = dirty_notes
        __['Dirty'] = dirty_notes.button_deck

        self.add_page(name, dirty_notes)

    def load_notes(self):
        """Load all notes that arent the DirtyNotes"""

        decks = __['Config'].get_decks()

        for name, deck_file in decks.items():
            self.add_page(name, ButtonGrid(deck_file))

    def add_page(self, title, _object):
        # page = Gtk.Box()
        # page.set_border_width(10)
        # page.add(_object)
        self.pages += [_object]
        self.append_page(wrap(_object), Gtk.Label(title))


@register_instance
class NewNote(Gtk.Grid):

    def __init__(self):
        Gtk.Grid.__init__(
            self, orientation=Gtk.Orientation.VERTICAL, hexpand=True, column_spacing=10, row_spacing=10)

        self.notes = __['Dirty']
        self.dirty_notes = __['DirtyNotes']

        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("Put name here or value will be used")

        self.save_button = Gtk.Button(label="QuickSave")
        self.save_button.connect('clicked', self.quick_save)

        self.save_form = Gtk.Button(label="Save")
        self.save_form.connect('clicked', self.save)

        self.textview = Gtk.TextView()
        self.textview.set_cursor_visible(True)
        self.textview.set_hexpand(True)
        self.textview.set_vexpand(False)
        self.textview.set_wrap_mode(Gtk.WrapMode.WORD)

        self.textbuffer = self.textview.get_buffer()
        self.textbuffer.set_text("")
        # textview.connect('focus', lambda x: x.grab_focus())
        self.wrapped_textview = wrap(self.textview)
        self.add(self.save_button)
        self.attach_next_to(self.entry, self.save_button,
                            Gtk.PositionType.RIGHT, 2, 1)

        self.attach_next_to(self.wrapped_textview, self.save_button,
                            Gtk.PositionType.BOTTOM, 2, 3)

        self.attach_next_to(self.save_form, self.wrapped_textview,
                            Gtk.PositionType.RIGHT, 2, 3)

    def clean_after(self):
        self.textbuffer.set_text("")
        self.entry.set_text("")

    def add_button(self, name, value):
        try:
            cabinet = __['FileCabinet']
            current_deck = cabinet.pages[cabinet.get_current_page()]
            b = current_deck.button_deck.add_button(name=name,
                                                    value=value)

            current_deck.add(b)
            b.show()
        except IndexError:
            pass  # yes, cause this value exists

    def quick_save(self, button):
        name = value = __['Jimmy'].recieve()

        if not value:
            logger.error("No value to save - aborting")
            self.clean_after()
            return False

        if self.entry.get_text().strip():
            name = self.entry.get_text().strip()

        self.add_button(name, value)
        self.clean_after()

    def edit(self, copy_button):
        dialog = DialogEdit(
            __['Application'].win,  copy_button)
        dialog.run()
        dialog.destroy()

    def save(self, button):
        value = self.textbuffer.get_text(
            self.textbuffer.get_start_iter(), self.textbuffer.get_end_iter(), False).strip()
        name = self.entry.get_text().strip()

        if not value:
            logger.error("No value to save - aborting")
            self.clean_after()
            return False

        if not name:
            dialog = DialogError(
                __['Application'].win, "Soo, the name is missing, it's required.")
            dialog.run()
            dialog.destroy()
        else:
            self.add_button(name, value)

        self.clean_after()
