from copypaster.widgets.buttons import CopyButton
from copypaster.file_loader import Deck
from copypaster.register import Register, register_instance

from copypaster import logger, CURRENT_DIR, State, NORMAL, AUTOSAVE, EDIT,  REMOVE
import time
import time
import sys
import os
import gettext
import datetime
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Gio  # noqa


# All translations provided for illustrative purposes only.
# english
def _(s): return s


CONTEXT = 'Button'


def wrap(widget):
    sw = Gtk.ScrolledWindow()
    sw.add(widget)
    # sw.set_policy(Gtk.PolicyType.AUTOMATIC,
    #              Gtk.PolicyType.AUTOMATIC)
    sw.set_border_width(1)
    return sw


class DialogError(Gtk.Dialog):

    def __init__(self, parent, massage):  # lol
        Gtk.Dialog.__init__(self)
        self.set_modal(True)
        self.add_button(button_text="OK", response_id=Gtk.ResponseType.OK)
        self.set_transient_for(parent)
        self.set_default_size(150, 100)

        label = Gtk.Label(massage)

        box = self.get_content_area()
        box.add(label)
        self.show_all()


class DialogEdit(Gtk.Dialog):

    def __init__(self, parent, button_to_edit):  # lol
        Gtk.Dialog.__init__(self)

        self.edited = button_to_edit

        self.set_modal(True)
        self.add_button(button_text="OK", response_id=Gtk.ResponseType.OK)
        self.add_button(button_text="CANCEL",
                        response_id=Gtk.ResponseType.CANCEL)
        self.set_transient_for(parent)
        self.set_default_size(450, 350)

        box = self.get_content_area()
        grid = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL,
                        hexpand=True, column_spacing=10, row_spacing=10)

        self.entry = Gtk.Entry()
        self.entry.set_text(self.edited.name)

        self.textview = Gtk.TextView()
        self.textview.set_cursor_visible(True)
        self.textview.set_hexpand(True)
        self.textview.set_vexpand(True)
        self.textview.set_wrap_mode(Gtk.WrapMode.WORD)

        self.textbuffer = self.textview.get_buffer()
        self.textbuffer.set_text(self.edited.value)

        self.wrapped_textview = wrap(self.textview)

        self.save_button = Gtk.Button(label="Save")
        self.save_button.connect('clicked', self.save)

        grid.add(self.entry)
        grid.add(self.wrapped_textview)
        grid.add(self.save_button)

        box.add(grid)

        self.show_all()

    def save(self, button):
        text_view_content = self.textbuffer.get_text(self.textbuffer.get_start_iter(
        ), self.textbuffer.get_end_iter(), False)

        self.edited.name, self.edited.value = self.entry.get_text(), text_view_content
        self.edited.set_label(self.edited.name)
        self.destroy()


class AnAction (Gio.SimpleAction):
    @classmethod
    def new(cls, name, parameter_type=None, callback=None):
        action = Gio.SimpleAction.new(name, parameter_type)
        action.enabled = True
        action.connect("activate", callback)    # TODO check this code
        return action


@register_instance
class StatusBar(Gtk.Statusbar):
    def __init__(self):
        Gtk.Statusbar.__init__(self)
        # TODO check whats with the context
        self.context_id = self.get_context_id(CONTEXT)

    def send(self, message):
        self.push(self.context_id, message)


@register_instance
class ToolBar(Gtk.Toolbar):
    "Sample toolbar provided by cookiecutter switch."

    def init_toolbutton(self, stock, callback, pos):
        button = Gtk.ToolButton(stock)
        button.set_is_important(True)
        # insert the button at position in the toolbar
        self.insert(button, pos)
        button.show()
        button.connect("clicked", callback)

    def __init__(self):
        # a toolbar
        Gtk.Toolbar.__init__(self)

        # which is the primary toolbar of the application
        self.get_style_context().add_class(Gtk.STYLE_CLASS_PRIMARY_TOOLBAR)
        self.set_hexpand(True)

        self.init_toolbutton(
            Gtk.STOCK_ADD, Register['Application'].add_new_notebook, 0)
        self.init_toolbutton(
            Gtk.STOCK_OPEN, Register['Application'].open_notebook, 1)
        self.init_toolbutton(
            Gtk.STOCK_SAVE, Register['Application'].save_current_notebook, 2)
        self.init_toolbutton(
            Gtk.STOCK_SAVE_AS, Register['Application'].saveas_current_notebook, 3)


@register_instance
class NewNote(Gtk.Grid):
    def __init__(self):
        Gtk.Grid.__init__(
            self, orientation=Gtk.Orientation.VERTICAL, hexpand=True, column_spacing=10, row_spacing=10)

        self.notes = Register['Dirty']
        self.dirty_notes = Register['DirtyNotes']

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
            cabinet = Register['FileCabinet']
            current_deck = cabinet.pages[cabinet.get_current_page()]
            b = current_deck.button_deck.add_button(name=name,
                                                    value=value)

            current_deck.add(b)
            b.show()
        except IndexError:
            pass  # yes, cause this value exists

    def quick_save(self, button):
        name = value = Register['Jimmy'].recieve()

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
            Register['Application'].win,  copy_button)
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
                Register['Application'].win, "Soo, the name is missing, it's required.")
            dialog.run()
            dialog.destroy()
        else:
            self.add_button(name, value)

        self.clean_after()


class StateButtonsCallbacks:
    def on_autosave(self, button, name):
        self._deactive_rest_buttons('autosave')

        if button.get_active():
            State['app'] = AUTOSAVE
            self.handle = self.clip.connect(
                'owner-change', self.auto_clipboard)
            logger.debug('Autosave on')
        else:
            State['app'] = NORMAL
            self.clip.disconnect(self.handle)
            logger.debug('Autosave off')

    def on_edit(self, button, name):
        self._deactive_rest_buttons('edit')

        if button.get_active():
            State['app'] = EDIT
            logger.debug('Edit on')
        else:
            State['app'] = NORMAL
            logger.debug('Edit off')

    def on_remove(self, button, name):
        self._deactive_rest_buttons('remove')

        if button.get_active():
            State['app'] = REMOVE
            logger.debug('Remove on')

        else:
            State['app'] = NORMAL
            logger.debug('Remove off')

    def auto_clipboard(self, clipboard, parameter):
        if State['app'] != AUTOSAVE:
            return False

        name = value = clipboard.wait_for_text()

        if not value:
            logger.error("No value to save - aborting")
            return False

        Register['NewNote'].add_button(name, value)

    def _deactive_rest_buttons(self, leave_alone):
        [button.set_active(False) for name, button in self.buttons.items(
        ) if name != leave_alone and button.get_active()]


@register_instance
class StateButtons(StateButtonsCallbacks, Gtk.Box):
    """Autosave, Edit, Remove"""

    def __init__(self):
        Gtk.Box.__init__(self, spacing=6)

        self.buttons = {}

        self.clip = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.handle = None

        self._create_button("Autosave", self.on_autosave, "1")
        self._create_button("Edit", self.on_edit, "2")
        self._create_button("Remove", self.on_remove, "3")

    def _create_button(self, name, callback, ind):
        _button = Gtk.ToggleButton(name)
        _button.connect("toggled", callback, ind)

        self.pack_start(_button, True, True, 0)

        self.buttons[name.lower()] = _button


@register_instance
class DirtyNotes(Gtk.FlowBox):
    "Main area of user interface content."

    def __init__(self):
        Gtk.FlowBox.__init__(self)

        self.button_deck = Register['Dirty']

        self.set_valign(Gtk.Align.START)
        self.set_max_children_per_line(4)
        self.set_selection_mode(Gtk.SelectionMode.NONE)

        for button in self.button_deck.get_buttons():
            self.add(button)

    def save_deck(self):
        self.button_deck.save_buttons()


class ButtonGrid(Gtk.FlowBox):
    "Main area of user interface content."

    def __init__(self, deck_file):
        Gtk.FlowBox.__init__(self)

        self.button_deck = Deck(deck_file)

        self.set_valign(Gtk.Align.START)
        self.set_max_children_per_line(4)
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

        self.add_page("Dirty notes", DirtyNotes())
        decks = Register['Config'].get_decks()

        for name, deck_file in decks.items():
            self.add_page(name, ButtonGrid(deck_file))

    def add_page(self, title, _object):
        # page = Gtk.Box()
        # page.set_border_width(10)
        # page.add(_object)
        self.pages += [_object]
        self.append_page(wrap(_object), Gtk.Label(title))


@register_instance
class MainFrame(Gtk.Grid):
    "Main area of user interface content."

    def __init__(self):
        Gtk.Grid.__init__(
            self, orientation=Gtk.Orientation.VERTICAL)
        # self.set_valign(Gtk.Align.START)
        self.file_cabinet = FileCabinet()
        self.adding = NewNote()
        self.state_buttons = StateButtons()
        self.add(self.state_buttons)
        self.add(self.adding)
        self.add(self.file_cabinet)


class AppCallbacks:
    # callback function for "new"
    def new_callback(self, action, parameter):
        print("This does nothing. It is only a demonstration.")

    # callback function for "about"
    def about_callback(self, action, parameter):
        dialog = Gtk.Dialog()
        dialog.set_title("A Gtk+ Dialog")
        dialog.set_transient_for(self)
        dialog.set_modal(True)
        dialog.add_button(button_text="OK", response_id=Gtk.ResponseType.OK)
        # connect the "response" signal (the button has been clicked) to the
        # function on_response()
        dialog.connect("response", self.on_response)

        # get the content area of the dialog, add a label to it
        content_area = dialog.get_content_area()
        label = Gtk.Label("This demonstrates a dialog with a label")
        content_area.add(label)
        # show the dialog
        dialog.show_all()

    def on_response(self, widget, response_id):
        print("response_id is %s" % response_id)
        # destroy the widget (the dialog) when the function on_response() is called
        # (that is, when the button of the dialog has been clicked)
        widget.destroy()

    # callback function for "quit"
    def quit_callback(self, action, parameter):
        print("You have quit.")
        self.quit()

    def add_new_notebook(self, action):
        pass

    def open_notebook(self, action):
        pass

    def save_current_notebook(self, action):
        cabinet = Register['FileCabinet']
        cabinet.pages[cabinet.get_current_page()].save_deck()

    def saveas_current_notebook(self, action):
        dialog = Gtk.FileChooserDialog(
            'Save button deck', self.win,
            Gtk.FileChooserAction.SAVE,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        dialog.set_do_overwrite_confirmation(True)
        if dialog.run() == Gtk.ResponseType.OK:
            filename = dialog.get_filename()

            cabinet = Register['FileCabinet']
            current_deck = cabinet.pages[cabinet.get_current_page()]

            try:
                current_deck.button_deck.path = filename
                current_deck.button_deck.save_buttons()
            except Exception as e:
                logger.error("There was an exception {}".format(e))
        dialog.destroy()

    def save_dirty_notebook(self, action):
        pass


@register_instance
class MainWindow(Gtk.ApplicationWindow):
    # constructor: the title is "Welcome to GNOME" and the window belongs
    # to the application app
    screen = None
    calculated_width = 0
    calculated_height = 0

    def __init__(self, app):
        Gtk.ApplicationWindow.__init__(
            self, title="CopyPaster", application=app)
        self.screen = self.get_screen()

        self.calculated_width = int((self.screen.get_width() / 100) * 20)
        self.calculated_height = self.screen.get_height()

        Register['calculated_width'] = self.calculated_width
        Register['calculated_height'] = self.calculated_height

        self.set_default_size(self.calculated_width, self.calculated_height)

        self.statusbar = StatusBar()
        self.statusbar.send("Waiting for you to do something...")

        # a toolbar created in the method create_toolbar (see below)
        self.toolbar = ToolBar()
        self.main = MainFrame()

        # grid
        self.grid = Gtk.Grid()
        self.grid.set_orientation(Gtk.Orientation.VERTICAL)
        # attach the toolbar to the grid
        self.grid.add(self.toolbar)
        self.grid.add(self.main)
        self.grid.add(self.statusbar)
        # add the grid to the window
        self.add(self.grid)

        self.toolbar.show() and self.main.show() and self.statusbar.show()
        # add status bar to some grid or shit


@register_instance
class Application(AppCallbacks, Gtk.Application):
    # constructor of the Gtk Application
    win = None

    def __init__(self):
        Gtk.Application.__init__(self)

        style_provider = Gtk.CssProvider()

        style_provider.load_from_path(os.path.join(CURRENT_DIR, "app.css"))

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        # self.set_app_menu(MenuBar())

        actions = [("new", self.new_callback,),
                   ("about", self.about_callback,),
                   ("quit", self.quit_callback,),

                   # ("app.add", self.add_new_notebook,),
                   # ("app.open", self.open_notebook,),
                   # ("app.save_current", self.save_current_notebook,),
                   # ("app.save_dirty_as", self.save_dirty_notebook,),
                   ]

        for action_name, callback in actions:
            action = AnAction.new(action_name, None, callback)
            self.add_action(action)

    # create and activate a MyWindow, with self (the MyApplication) as
    # application the window belongs to.
    # Note that the function in C activate() becomes do_activate() in Python
    def do_activate(self):
        self.win = MainWindow(self)
        # show the window and all its content
        # this line could go in the constructor of MyWindow as well
        self.win.show_all()
        State['app'] = NORMAL

    # start up the application
    # Note that the function in C startup() becomes do_startup() in Python
    def do_startup(self):
        Gtk.Application.do_startup(self)
