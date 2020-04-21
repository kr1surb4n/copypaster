from copypaster.widgets.notebooks import FileCabinet, NewNote
from copypaster.widgets.toolbar import ToolBar
from copypaster.widgets.statebuttons import StateButtons
from copypaster.widgets.utility import AnAction
from copypaster.signal_bus import signal_bus

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


@register_instance
class StatusBar(Gtk.Statusbar):
    def __init__(self):
        Gtk.Statusbar.__init__(self)
        # TODO check whats with the context
        self.context_id = self.get_context_id(CONTEXT)

    def send(self, message):
        self.push(self.context_id, message)


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

        self.main = MainFrame()

        # grid
        self.grid = Gtk.Grid()
        self.grid.set_orientation(Gtk.Orientation.VERTICAL)
        self.grid.add(self.main)
        self.add(self.grid)

        self.main.show()
        

@register_instance
class MainFrame(Gtk.Grid):
    "Main area of user interface content."

    def __init__(self):
        Gtk.Grid.__init__(
            self, orientation=Gtk.Orientation.VERTICAL)
        # self.set_valign(Gtk.Align.START)
        self.file_cabinet = FileCabinet()
        self.adding = NewNote()
        self.state_buttons = StateButtons(State)
        self.add(self.state_buttons)
        self.add(self.adding)
        self.add(self.file_cabinet)


class AppCallbacks:
    def new_notebook(self, action):
        signal_bus.emit('new_notebook')
        pass

    def open_notebook(self, action):
        signal_bus.emit('open_notebook')
        pass

    def save_notebook(self, action):
        signal_bus.emit('save_notebook')

        cabinet = Register['FileCabinet']
        cabinet.pages[cabinet.get_current_page()].save_deck()

    def save_notebook_as(self, action):
        signal_bus.emit('save_notebook_as')

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

    def handle_quit(self, action, parameter):
        signal_bus.emit('quit')
        self.quit()


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

        # this all is a lot of work, I would do something with it
        actions = [("new_notebook", self.new_notebook,),
                   ("open_notebook", self.open_notebook,),
                   ("save_notebook", self.save_notebook,),
                   ("save_notebook_as", self.save_notebook_as,),
                   ("quit", self.handle_quit,), ]

        for action_name, callback in actions:
            action = AnAction.new(action_name, None, callback)
            self.add_action(action)

    def do_activate(self):
        self.win = MainWindow(self)
        self.win.show_all()
        State['app'] = NORMAL

    def do_startup(self):
        Gtk.Application.do_startup(self)

        # create a menu
        menu = Gio.Menu()
        # append to the menu three options
        menu.append("New notebook", "app.new_notebook")
        menu.append("Open notebook", "app.open_notebook")
        menu.append("Save notebook", "app.save_notebook")
        menu.append("Save notebook as", "app.save_notebook_as")
        menu.append("Quit", "app.quit")
        # set the menu as menu of the application
        self.set_app_menu(menu)
