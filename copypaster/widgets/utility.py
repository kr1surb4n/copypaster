import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Gio  # noqa


def wrap(widget):
    sw = Gtk.ScrolledWindow()
    sw.add(widget)
    # sw.set_policy(Gtk.PolicyType.AUTOMATIC,
    #              Gtk.PolicyType.AUTOMATIC)
    sw.set_border_width(1)
    return sw


class AnAction (Gio.SimpleAction):
    @classmethod
    def new(cls, name, parameter_type=None, callback=None):
        action = Gio.SimpleAction.new(name, parameter_type)
        action.enabled = True
        action.connect("activate", callback)    # TODO check this code
        return action
