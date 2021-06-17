import os

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Gio  # noqa


# default_provider = Gtk.CssProvider()


def test_main():
    assert True


def test_style_providers():
    import app

    app.CURRENT_DIR = os.path.dirname(__file__)

    button = Gtk.Button(label="No")
    # context = button.get_style_context()

    from app.style import (
        default_style_context,
        load_default_styles,
        reload_default_styles,
        load_style,
    )

    load_default_styles()

    assert default_style_context
    assert isinstance(default_style_context, Gtk.StyleContext)
    assert default_style_context.has_class("test")

    load_style(os.path.join(app.CURRENT_DIR, "style.css"))

    assert context.has_class("loaded")
