from copypaster.register import Register, register_instance
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Gio  # noqa


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

    def __init__(self, reg):
        # a toolbar
        Gtk.Toolbar.__init__(self)
        self.reg = reg

        # which is the primary toolbar of the application
        self.get_style_context().add_class(Gtk.STYLE_CLASS_PRIMARY_TOOLBAR)
        self.set_hexpand(True)

        self.init_toolbutton(
            Gtk.STOCK_ADD, reg['Application'].add_new_notebook, 0)
        self.init_toolbutton(
            Gtk.STOCK_OPEN, reg['Application'].open_notebook, 1)
        self.init_toolbutton(
            Gtk.STOCK_SAVE, reg['Application'].save_current_notebook, 2)
        self.init_toolbutton(
            Gtk.STOCK_SAVE_AS, reg['Application'].saveas_current_notebook, 3)
