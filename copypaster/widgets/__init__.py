from copypaster.widgets.buttons import CopyButton
from copypaster.register import Register, register_instance

from copypaster import logger, CURRENT_DIR
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


class AnAction (Gio.SimpleAction):
    @classmethod
    def new(cls, name, parameter_type=None, callback=None):
        action = Gio.SimpleAction.new(name, parameter_type)
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

    def __init__(self):
        # a toolbar
        Gtk.Toolbar.__init__(self)

        # which is the primary toolbar of the application
        self.get_style_context().add_class(Gtk.STYLE_CLASS_PRIMARY_TOOLBAR)
        self.set_hexpand(True)
        # create a button for the "new" action, with a stock image
        new_button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_NEW)
        # label is shown
        new_button.set_is_important(True)
        # insert the button at position in the toolbar

        self.insert(new_button, 0)
        # show the button
        new_button.show()
        # set the name of the action associated with the button.
        # The action controls the application (app)
        new_button.set_action_name("app.new")
        """
        # button for the "open" action
        open_button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_OPEN)
        open_button.set_is_important(True)
        self.insert(open_button, 1)
        open_button.show()
        open_button.set_action_name("app.open")

        # button for the "undo" action
        undo_button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_UNDO)
        undo_button.set_is_important(True)
        self.insert(undo_button, 2)
        undo_button.show()
        undo_button.set_action_name("win.undo")

        # button for the "fullscreen/leave fullscreen" action
        self.fullscreen_button = Gtk.ToolButton.new_fro _stock(
            Gtk.STOCK_FULLSCREEN)
        self.fullscreen_button.set_is_important(True)
        self.insert(self.fullscreen_button, 3)
        self.fullscreen_button.set_action_name("win.fullscreen")
        """


class NewNote(Gtk.FlowBox):
    def __init__(self):
        Gtk.ListBox.__init__(self)
        self.init_forms()

    def init_forms(self):

        save_button = Gtk.Button(label="save from paste")
        save_form = Gtk.Button(label="save from form")

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)

        textview = Gtk.TextView()
        textbuffer = textview.get_buffer()
        textbuffer.set_text("")

        self.add(save_button)

        scrolledwindow.add(textview)
        box.add(scrolledwindow)
        #box.pack_start(save_form, False, True, 0)

        self.add(box)
        # textview.grab_focus()


@register_instance
class DirtyNotes(Gtk.FlowBox):
    "Main area of user interface content."

    def __init__(self):
        Gtk.FlowBox.__init__(self)

        self.set_valign(Gtk.Align.START)
        self.set_max_children_per_line(4)
        self.set_selection_mode(Gtk.SelectionMode.NONE)

        for kwargs in Register['Simple'].get_buttons():
            button = CopyButton(**kwargs)
            self.add(button)

    def init_forms(self):
        pass


@register_instance
class ButtonGrid(Gtk.FlowBox):
    "Main area of user interface content."

    def __init__(self, buttons):
        Gtk.FlowBox.__init__(self)

        self.set_valign(Gtk.Align.START)
        self.set_max_children_per_line(4)
        self.set_selection_mode(Gtk.SelectionMode.NONE)

        for kwargs in Register[buttons].get_buttons():
            button = CopyButton(**kwargs)
            self.add(button)

    def load_buttons(self):
        pass


@register_instance
class FileCabinet(Gtk.Notebook):
    """Here we keep the buttons grids and stuff"""

    def __init__(self):
        Gtk.Notebook.__init__(self)
        self.pages = []

        self.add_page("Dirty notes", DirtyNotes())
        self.add_page("Simple", ButtonGrid('Simple'))
        self.add_page("Python", ButtonGrid('Python'))
        self.add_page("Bash", ButtonGrid('Bash'))

    def add_page(self, title, _object):
        #page = Gtk.Box()
        # page.set_border_width(10)
        # page.add(_object)
        self.pages += [_object]
        self.append_page(_object, Gtk.Label(title))


@register_instance
class MainFrame(Gtk.ListBox):
    "Main area of user interface content."

    def __init__(self):
        Gtk.ListBox.__init__(self)

        # self.set_valign(Gtk.Align.START)
        self.file_cabinet = FileCabinet()
        self.add(self.file_cabinet)


class AppCallbacks:
    # callback function for "new"
    def new_callback(self, action, parameter):
        print("This does nothing. It is only a demonstration.")

    # callback function for "about"
    def about_callback(self, action, parameter):
        print("No AboutDialog for you. This is only a demonstration.")
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


@register_instance
class MainWindow(Gtk.ApplicationWindow):
    # constructor: the title is "Welcome to GNOME" and the window belongs
    # to the application app
    screen = None
    calculated_width = 0
    calculated_height = 0

    def __init__(self, app):
        Gtk.Window.__init__(self, title="CopyPaster", application=app)
        self.screen = self.get_screen()

        self.calculated_width = int((self.screen.get_width() / 100) * 20)
        self.calculated_height = self.screen.get_height()

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
                   ("quit", self.quit_callback,)]

        for action_name, callback in actions:
            action = AnAction.new(action_name, None, callback)
            self.add_action(action)

    # create and activate a MyWindow, with self (the MyApplication) as
    # application the window belongs to.
    # Note that the function in C activate() becomes do_activate() in Python
    def do_activate(self):
        win = MainWindow(self)
        # show the window and all its content
        # this line could go in the constructor of MyWindow as well
        win.show_all()

    # start up the application
    # Note that the function in C startup() becomes do_startup() in Python
    def do_startup(self):
        Gtk.Application.do_startup(self)
