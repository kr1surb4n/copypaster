import gi


gi.require_version("Gtk", "3.0")
from gi.repository import Gtk  # noqa


def test_wrap():
    from app.utility import wrap
    
    """Test if the object wrapped is Gtk.ScrolledWindow"""
    wrapper = wrap(Gtk.Label(label="Puf"))

    assert isinstance(wrapper, Gtk.ScrolledWindow)

    children = wrapper.get_children()[0].get_children()
    assert len(children) == 1
    assert isinstance(children[0], Gtk.Label)
