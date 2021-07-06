from app.register import register_instance

from app import log, CURRENT_DIR
import os

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GObject  # noqa


@register_instance
class Style:
    def __init__(self):
        self.registry = []
        self.default_provider = Gtk.CssProvider()

    def load_styles_from_files(self):
        log.info("Loading css files")
        for path_to_css in self.registry:
            self.default_provider.load_from_path(path_to_css)

    def reset_styles(self):
        log.info("Reseting styles")
        Gtk.StyleContext.remove_provider_for_screen(
            Gdk.Screen.get_default(), self.default_provider
        )

        self.default_provider = Gtk.CssProvider()

        self.load_styles()

    def load_styles(self):
        log.info("Loading styles")
        self.load_styles_from_files()

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            self.default_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

        Gtk.StyleContext.reset_widgets(Gdk.Screen.get_default())


style = Style()


def test_styles():
    style = Style()
    assert style

    style.registry.append(os.path.join(CURRENT_DIR, "styles/app.css"))
    assert len(style.registry) == 1

    style.load_styles()

    label = Gtk.Label(label="text")
    style_context = label.get_style_context()

    color = style_context.get_color(Gtk.StateFlags.NORMAL)
    assert color.blue == 1.0 and color.red == 0.0 and color.green == 0.0

    style.registry.append(os.path.join(CURRENT_DIR, "styles/test.css"))
    assert len(style.registry) == 2

    style.reset_styles()
    color = style_context.get_color(Gtk.StateFlags.NORMAL)
    assert color.blue == 0.0 and color.red == 1.0 and color.green == 0.0
