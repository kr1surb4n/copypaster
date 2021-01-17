from app.signal_bus import subscribe
from app.register import Register as __

from app import log, CURRENT_DIR
import os

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Gio  # noqa


default_provider = Gtk.CssProvider()


@subscribe
def load_default_styles():
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
