from app.style import Style

import os
from os.path import join, dirname
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GObject  # noqa


def test_styles():
    label = Gtk.Label(label="text")
    style_context = label.get_style_context()
    
    style = Style()
    assert style
    
    style.registry.append(join(dirname(__file__), 'styles/app.css'))
    assert len(style.registry) == 1

    style.load_styles()

    # see if it's red
    color = style_context.get_color(Gtk.StateFlags.NORMAL)
    assert color.blue == 1.0 and color.red == 0.0 and color.green == 0.0

    # add test css
    style.registry.append(join(dirname(__file__), 'styles/test.css'))
    assert len(style.registry) == 2

    style.reset_styles()

    # see if it's blue
    color = style_context.get_color(Gtk.StateFlags.NORMAL)
    assert color.blue == 0.0 and color.red == 1.0 and color.green == 0.0

    # reset all
    style.registry = []
    style.registry.append(join(dirname(__file__), 'styles/app.css'))
    assert len(style.registry) == 1    
    style.reset_styles()

    color = style_context.get_color(Gtk.StateFlags.NORMAL)
    assert color.blue == 1.0 and color.red == 0.0 and color.green == 0.0
