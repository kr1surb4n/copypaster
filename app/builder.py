# -*- coding: utf-8 -*-
from app import log
from app.register import register_instance

""" Initialize services """

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gtk  # noqa

@register_instance
class Builder(Gtk.Builder):
    """This extends the Gtk.Builder, so that
    you can register a custom type during init,
    and before loading Glade file"""

    def __init__(self, *args, **kwargs):
        self.custom_objects = {}
        super(Gtk.Builder, self).__init__(*args, **kwargs)

    def add_custom_object(self, name, widget_type):
        log.info(f"Builder: Adding {name} for {widget_type}")
        self.custom_objects[name] = widget_type

    def do_get_type_from_name(self, type_name):
        log.info(f"Builder: Resolving object for type {type_name}")
        """
        Looks up a type by name, using the virtual function that Gtk.Builder
        has for that purpose.

        searches the type in `self.custom_objects` dictionaries.


        Parameters:  type_name (str) – type name to lookup
        Returns:     the GObject.GType found for type_name
                       or GObject.TYPE_INVALID if no type was found
        Return type: GObject.GType

        """

        if type_name in self.custom_objects:
            return self.custom_objects[type_name]

        r = Gtk.Builder.do_get_type_from_name(self, type_name)
        print('GtkBuilder: => {}\t{}'.format(type_name, r))
        return r


builder = Builder()


def test_builder_happy_path():
    builder = Builder()

    missing = 'missing'
    mycustomtype = 'mycustomtype'

    class MyCustomType:
        ...

    builder.add_custom_object(mycustomtype, MyCustomType)

    assert builder.do_get_type_from_name(mycustomtype) == MyCustomType
    assert isinstance(builder.do_get_type_from_name(missing), GObject.GType)
