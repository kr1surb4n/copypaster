from folders.widgets.notebooks import FileCabinet
from folders.widgets.statebuttons import StateButtons
from folders.widgets.utility import AnAction
from folders.signal_bus import signal_bus

from folders.register import Register as __, register_instance

from folders import log, CURRENT_DIR, State, AppState
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
    file_cabinet = adding = state_buttons = None


    screen = None
    calculated_width = 0
    calculated_height = 0

    def __init__(self, app):
        Gtk.ApplicationWindow.__init__(
            self, title="CopyPaster", application=app)
        log.debug("Calculating screen size...")
        self.screen = self.get_screen()

        self.calculate_size()

        self.set_default_size(self.calculated_width, self.calculated_height)

        self.set_resize_mode(Gtk.ResizeMode.PARENT)
        log.debug("Loading main objects...")


        self.file_cabinet = FileCabinet()
        #self.state_buttons = StateButtons()


        self.add(self.file_cabinet)

    def calculate_size(self):
        self.calculated_width = self.screen.get_width()
        self.calculated_height = self.screen.get_height()

        __['calculated_width'] = self.calculated_width
        __['calculated_height'] = self.calculated_height




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
        log.debug("Emitting new_notebook...")
        signal_bus.emit('new_notebook')

    def open_notebook(self, action):
        log.debug("Emitting open_notebook...")
        signal_bus.emit('open_notebook')

    def save_notebook(self, action, asd):
        log.debug("Emitting save_notebook...")
        signal_bus.emit('save_notebook')

    def save_notebook_as(self, action, asd):
        log.debug("Emitting save_notebook_as...")

    def handle_quit(self, action, parameter):
        log.debug("Emitting quit...")

        signal_bus.emit('quit')
        self.quit()
        log.debug("Goodbye! Application terminated.")



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
        log.debug("Lift off!")
        self.win = MainWindow(self)
        self.win.show_all()

        log.debug("App state NORMAL")
        AppState['app'] = State.NORMAL

        log.debug("Emitting start_app...")
        signal_bus.emit('start_app')

        log.debug("All green. Welcome to application.")

    def do_startup(self):
        log.debug("Startup...")
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
        log.debug('Menu loaded...')
