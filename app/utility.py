import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk  # noqa


def wrap(widget):
    """Scrollwindow wrapper"""
    sw = Gtk.ScrolledWindow()
    sw.add(widget)
    sw.set_border_width(1)
    return sw
