
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk  # noqa



class CustomWidget(Gtk.Label):
    ...

CUSTOM_WIDGET = 'CustomWidget'
TEST_GLADE_FILE = 'example_custom.glade'

def test_builder_fails_without_custom_class():

    from app.builder import builder 

    try:
        builder.add_from_file(TEST_GLADE_FILE)  
        assert False
    except gi.repository.GLib.GError:
        "No CustomWidget"
        assert True


def test_builder_custom_widget():

    from app.builder import builder 

    builder.add_custom_object(CUSTOM_WIDGET, CustomWidget)
    builder.add_from_file(TEST_GLADE_FILE)  

    widget = builder.get_object(CUSTOM_WIDGET)
    assert widget