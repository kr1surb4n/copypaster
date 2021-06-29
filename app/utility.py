import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk  # noqa


def wrap(widget):
    """Scrollwindow wrapper"""
    sw = Gtk.ScrolledWindow()
    sw.add(widget)
    sw.set_border_width(1)
    return sw


def test_wrap():
    """Test if the object wrapped is Gtk.ScrolledWindow"""
    wrapper = wrap(Gtk.Label(label="Puf"))

    assert isinstance(wrapper, Gtk.ScrolledWindow)

    children = wrapper.get_children()[0].get_children()
    assert len(children) == 1
    assert isinstance(children[0], Gtk.Label)