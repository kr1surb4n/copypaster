from app.signal_bus import subscribe
from app.register import Register as __

from app import log, CURRENT_DIR
import os

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Gio  # noqa


styles_register = {}
default_provider = Gtk.CssProvider()

# TODO redesign everything here.
"""
i need to have:
- style_register, a list/hash, with paths to css files
- a default style added to style_register
- a function to add file to  style_register
- a function to load the styles
- a function to reload the styles

"""


@subscribe
def load_styles():
    global default_provider
    default_provider.load_from_path(os.path.join(CURRENT_DIR, "app.css"))

    Gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(),
        default_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
    )


@subscribe
def load_style(filepath):
    global default_provider
    Gtk.StyleContext.remove_provider_for_screen(
        Gdk.Screen.get_default(), default_provider
    )

    default_provider = Gtk.CssProvider()
    default_provider.load_from_path(filepath)

    Gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(),
        default_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
    )

    Gtk.StyleContext.reset_widgets(Gdk.Screen.get_default())


@subscribe
def reload_default_styles():
    global default_provider
    Gtk.StyleContext.remove_provider_for_screen(
        Gdk.Screen.get_default(), default_provider
    )

    default_provider = Gtk.CssProvider()
    default_provider.load_from_path(os.path.join(CURRENT_DIR, "app.css"))

    Gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(),
        default_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
    )

    Gtk.StyleContext.reset_widgets(Gdk.Screen.get_default())

log.info("Styles loaded")

def test_styles():
    raise NotImplementedError("styles need tests")
