from copypaster.widgets.notebooks import FileCabinet, NewNote
from copypaster.widgets.toolbar import ToolBar
from copypaster.widgets.statebuttons import StateButtons
from copypaster.widgets.utility import AnAction


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

        #self.statusbar = StatusBar()
        #self.statusbar.send("Waiting for you to do something...")

        # a toolbar created in the method create_toolbar (see below)
        self.toolbar = ToolBar(Register)
        self.main = MainFrame()

        # grid
        self.grid = Gtk.Grid()
        self.grid.set_orientation(Gtk.Orientation.VERTICAL)
        # attach the toolbar to the grid
        self.grid.add(self.toolbar)
        self.grid.add(self.main)
        # self.grid.add(self.statusbar)
        # add the grid to the window
        self.add(self.grid)

        self.toolbar.show() and self.main.show()  # and self.statusbar.show()
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
