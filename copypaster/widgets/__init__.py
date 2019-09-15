import datetime
import gettext
import sys
import time
import tkinter
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio

# All translations provided for illustrative purposes only.
 # english
_ = lambda s: s


class StatusBar(Gtk.Statusbar):
    def __init__(self):
        Gtk.Statusbar.__init__(self)


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
        self.fullscreen_button = Gtk.ToolButton.new_from_stock(
            Gtk.STOCK_FULLSCREEN)
        self.fullscreen_button.set_is_important(True)
        self.insert(self.fullscreen_button, 3)
        self.fullscreen_button.set_action_name("win.fullscreen")
        """

class MainFrame(Gtk.FlowBox):
    "Main area of user interface content."

    def __init__(self):
        Gtk.FlowBox.__init__(self)

        self.set_valign(Gtk.Align.START)
        self.set_max_children_per_line(3)
        self.set_selection_mode(Gtk.SelectionMode.NONE)

        for i in range(6):
            _button_text = 'Button %s' % i
            button = Gtk.Button(label=_button_text)
            self.add(button)

class MenuBar(Gio.Menu):
    "Menu bar appearing with expected components."

    def __init__(self):
        Gio.Menu.__init__(self)

        self.append("New", "app.new")
        self.append("About", "app.about")
        self.append("Quit", "app.quit")


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
        print( "response_id is %s" % response_id)
        # destroy the widget (the dialog) when the function on_response() is called
        # (that is, when the button of the dialog has been clicked)
        widget.destroy()

    # callback function for "quit"
    def quit_callback(self, action, parameter):
        print("You have quit.")
        self.quit()


class MainWindow(Gtk.ApplicationWindow):
    # constructor: the title is "Welcome to GNOME" and the window belongs
    # to the application app

    def __init__(self, app):
        Gtk.Window.__init__(self, title="Welcome to GNOME", application=app)

        self.statusbar = StatusBar()
        self.context_id = self.statusbar.get_context_id("example")
        self.statusbar.push(
            self.context_id, "Waiting for you to do something...")

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

        self.toolbar.show()
        self.main.show()
        self.statusbar.show()
        # add status bar to some grid or shit

class Application(AppCallbacks, Gtk.Application):
    # constructor of the Gtk Application

    def __init__(self):
        Gtk.Application.__init__(self)

        self.set_app_menu(MenuBar())


        actions = [("new", self.new_callback,),
        ("about", self.about_callback,),
        ("quit", self.quit_callback,)]

        for action_name, callback in actions:
            action = Gio.SimpleAction.new(action_name, None)
            action.connect("activate", callback)
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


if __name__ == '__main__':
    # create and run the application, exit with the value returned by
    # running the program
    app = Application()
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)
