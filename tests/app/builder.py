# -*- coding: utf-8 -*-

import gi
from os.path import join, dirname

gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gtk  # noqa


def test_builder_custom_widget():
    from app.builder import Builder

    # given
    class CustomWidget(Gtk.Label):
        ...

    CUSTOM_WIDGET = 'CustomWidget'
    TEST_GLADE_FILE = join(dirname(dirname(__file__)), 'fixtures/example_custom.glade')

    builder = Builder()

    # when
    builder.add_custom_object(CUSTOM_WIDGET, CustomWidget)
    builder.add_from_file(TEST_GLADE_FILE)

    # then
    widget = builder.get_object(CUSTOM_WIDGET)
    assert widget
    assert isinstance(widget, CustomWidget)


def test_if_builder_fails_without_a_custom_class():
    from app.builder import Builder

    TEST_GLADE_FILE = join(dirname(dirname(__file__)), 'fixtures/example_custom.glade')

    builder = Builder()

    try:
        builder.add_from_file(TEST_GLADE_FILE)
        assert False
    except gi.repository.GLib.GError:
        "No CustomWidget"
        assert True


def test_builder_happy_path():
    from app.builder import Builder

    # given
    missing = 'missing'
    mycustomtype = 'mycustomtype'

    class MyCustomType:
        ...

    builder = Builder()
    
    # when
    builder.add_custom_object(mycustomtype, MyCustomType)

    # then there is one custom object
    assert len(builder.custom_objects) == 1

    # and it's our custom object
    assert mycustomtype in builder.custom_objects

    # and missing is not in custom object 
    assert not missing in builder.custom_objects


    # when we want type from name
    type_returned = builder.do_get_type_from_name(mycustomtype)
    
    # then
    assert type_returned == MyCustomType
    # and
    assert isinstance(builder.do_get_type_from_name(missing), GObject.GType)

