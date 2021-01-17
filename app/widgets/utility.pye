import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Gio  # noqa


def wrap(widget):
    sw = Gtk.ScrolledWindow()
    sw.add(widget)
    # sw.set_policy(Gtk.PolicyType.AUTOMATIC,
    #              Gtk.PolicyType.AUTOMATIC)
    sw.set_border_width(1)
    return sw
