import datetime
import gettext
import sys
import time
import tkinter
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename
from gi.repository import Gtk, Gio

# All translations provided for illustrative purposes only.
 # english
_ = lambda s: s



class PopupDialog(ttk.Frame):
    "Sample popup dialog implemented to provide feedback."

    def __init__(self, parent, title, body):
        ttk.Frame.__init__(self, parent)
        self.top = tkinter.Toplevel(parent)
        _label = ttk.Label(self.top, text=body, justify=tkinter.LEFT)
        _label.pack(padx=10, pady=10)
        _button = ttk.Button(self.top, text=_("OK"), command=self.ok_button)
        _button.pack(pady=5)
        self.top.title(title)

    def ok_button(self):
        "OK button feedback."

        self.top.destroy()



class NavigationBar(ttk.Frame):
    "Sample navigation pane provided by cookiecutter switch."

    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.config(border=1, relief=tkinter.GROOVE)

        self.scrollbar = ttk.Scrollbar(self, orient=tkinter.VERTICAL)
        self.scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y, expand=1)

        self.listbox = tkinter.Listbox(self, bg='white')
        self.listbox.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
        for i in range(1, 100):
            self.listbox.insert(tkinter.END, _('Navigation ') + str(i))
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)
        self.bind_all('<<ListboxSelect>>', self.onselect)
        self.pack()

    def onselect(self, event):
        """Sample function provided to show how navigation commands may be \
        received."""

        widget = event.widget
        _index = int(widget.curselection()[0])
        _value = widget.get(_index)
        print(_('List item'), ' %d / %s' % (_index, _value))


        self.statusbar = Gtk.Statusbar()
        # its context_id - not shown in the UI but needed to uniquely identify
        # the source of a message
        self.context_id = self.statusbar.get_context_id("example")
        # we push a message onto the statusbar's stack
        self.statusbar.push(
            self.context_id, "Waiting for you to do something...")

class StatusBar(Gtk.StatusBar):

    def __init__(self):
        Gtk.StatusBar.__init__(self)


class ToolBar(ttk.Frame):
    "Sample toolbar provided by cookiecutter switch."

    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.buttons = []
        self.config(border=1, relief=tkinter.GROOVE)
        for i in range(1, 5):
            _button_text = _('Tool ') + str(i)
            self.buttons.append(ttk.Button(self, text=_button_text,
                                           command=lambda i=i:
                                           self.run_tool(i)))
            self.buttons[i - 1].grid(row=0)

    def run_tool(self, number):
        "Sample function provided to show how a toolbar command may be used."

        print(_('Toolbar button'), number, _('pressed'))



class MainFrame(ttk.Frame):
    "Main area of user interface content."

    past_time = datetime.datetime.now()

    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)

        self.buttons = []

        j = 0
        _buttons_in_row = 6
        for i in range(81):
            column = i % _buttons_in_row + 1
            _button_text = 'Button %s' % column
            _is_start = i == 0
            self.buttons.append(ttk.Button(self, text=_button_text,
                                           command=None))
            self.buttons[i - 1].grid(row=j, column=column, sticky=tkinter.W) # , fill=tkinter.X
            # self.buttons[i - 1].pack(side=tkinter.LEFT, padx=5, pady=3) # , fill=tkinter.X

            if i % _buttons_in_row == 0 and not _is_start:
                j += 1


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

    # callback function for "quit"
    def quit_callback(self, action, parameter):
        print("You have quit.")
        self.quit()


class MainWindow(AppCallbacks, Gtk.ApplicationWindow):
    # constructor: the title is "Welcome to GNOME" and the window belongs
    # to the application app

    def __init__(self, app):
        Gtk.Window.__init__(self, title="Welcome to GNOME", application=app)

        self.set_app_menu(MenuBar())


        actions = [("new", self.new_callback,),
        ("about", self.about_callback,),
        ("quit", self.quit_callback,)]

        for action_name, callback in actions:
            action = Gio.SimpleAction.new(action_name, None)
            action.connect("activate", callback)
            self.add_action(action)

        statusbar = StatusBar()
        self.context_id = statusbar.get_context_id("example")

        statusbar.push(
            self.context_id, "Waiting for you to do something...")

        # add status bar to some grid or shit

class Application(Gtk.Application):
    # constructor of the Gtk Application

    def __init__(self):
        Gtk.Application.__init__(self)

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




class Application(tkinter.Tk):
    "Create top-level Tkinter widget containing all other widgets."

    def __init__(self):
        tkinter.Tk.__init__(self)
        menubar = MenuBar(self)
        self.config(menu=menubar)
        self.wm_title('Py3 Tkinter')
        self.wm_geometry('640x480')

# Status bar selection == 'y'
        self.statusbar = StatusBar(self)
        self.statusbar.grid(row=2)
        self.bind_all('<Enter>', lambda e: self.statusbar.set_text(0,
                      'Mouse: 1'))
        self.bind_all('<Leave>', lambda e: self.statusbar.set_text(0,
                      'Mouse: 0'))
        self.bind_all('<Button-1>', lambda e: self.statusbar.set_text(1,
                      'Clicked at x = ' + str(e.x) + ' y = ' + str(e.y)))
        self.start_time = datetime.datetime.now()
        self.uptime()

# Tool bar selection == 'y'
        self.toolbar = ToolBar(self)
        self.toolbar.grid(row=0)


        self.mainframe = MainFrame(self)
        self.mainframe.grid(row=1)

# Status bar selection == 'y'
    def uptime(self):
        _upseconds = str(int(round((datetime.datetime.now() - self.start_time).total_seconds())))
        self.statusbar.set_text(2, _('Uptime') + ': ' + _upseconds)
        self.after(1000, self.uptime)


if __name__ == '__main__':
    # create and run the application, exit with the value returned by
    # running the program
    app = Application()
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)
