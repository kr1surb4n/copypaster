from copypaster.widgets.notebooks import FileCabinet
from copypaster.widgets.statebuttons import StateButtons
from copypaster.widgets.utility import AnAction
from copypaster.signal_bus import signal_bus

from copypaster.register import Register as __, register_instance

from copypaster import logger, CURRENT_DIR, State, AppState
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


@register_instance
class MainWindow(Gtk.ApplicationWindow):
    # constructor: the title is "Welcome to GNOME" and the window belongs
    # to the application app


    # constructor of the Gtk Application
    file_cabinet = adding = state_buttons = None


    screen = None
    calculated_width = 0
    calculated_height = 0

    def __init__(self, app):
        Gtk.ApplicationWindow.__init__(
            self, title="CopyPaster", application=app)
        logger.debug("Calculating screen size...")
        self.screen = self.get_screen()

        self.calculated_width = int((self.screen.get_width() / 100) * 20)
        self.calculated_height = self.screen.get_height()

        __['calculated_width'] = self.calculated_width
        __['calculated_height'] = self.calculated_height

        self.set_default_size(self.calculated_width, self.calculated_height)

        logger.debug("Loading main objects...")
        # grid
        self.grid = Gtk.Grid()
        self.grid.set_orientation(Gtk.Orientation.VERTICAL)

        self.file_cabinet = FileCabinet()
        self.state_buttons = StateButtons()

        self.grid.add(self.state_buttons)
        self.grid.add(self.file_cabinet)

        self.add(self.grid)



class AppCallbacks:

    def _init_actions(self):
        # this all is a lot of work, I would do something with it
        actions = [("new_notebook", self.new_notebook,),
                   ("open_notebook", self.open_notebook,),
                   ("save_notebook", self.save_notebook,),
                   ("save_notebook_as", self.save_notebook_as,),
                   ("quit", self.handle_quit,), ]

        for action_name, callback in actions:
            action = AnAction.new(action_name, None, callback)
            self.add_action(action)

    def new_notebook(self, action):
        logger.debug("Emitting new_notebook...")
        signal_bus.emit('new_notebook')

    def open_notebook(self, action):
        logger.debug("Emitting open_notebook...")
        signal_bus.emit('open_notebook')

    def save_notebook(self, action):
        logger.debug("Emitting save_notebook...")
        signal_bus.emit('save_notebook')

    def save_notebook_as(self, action):
        logger.debug("Emitting save_notebook_as...")

    def handle_quit(self, action, parameter):
        logger.debug("Emitting quit...")

        signal_bus.emit('quit')
        self.quit()
        logger.debug("Goodbye! Application terminated.")



@register_instance
class Application(AppCallbacks, Gtk.Application):

    win = None

    def __init__(self):
        Gtk.Application.__init__(self)
        self._init_actions()

        style_provider = Gtk.CssProvider()
        style_provider.load_from_path(os.path.join(CURRENT_DIR, "app.css"))

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def do_activate(self):
        logger.debug("Lift off!")
        self.win = MainWindow(self)
        self.win.show_all()

        logger.debug("App state NORMAL")
        AppState['app'] = State.NORMAL

        logger.debug("Emitting start_app...")
        signal_bus.emit('start_app')

        logger.debug("All green. Welcome to application.")

    def do_startup(self):
        logger.debug("Startup...")
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
        logger.debug('Menu loaded...')
