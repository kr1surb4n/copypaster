from app.register import Register as __
from app.signal_bus import emit, event
from app import log
import logging
from os.path import join, dirname
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GObject  # noqa

# load the functions
from app.stories import application

def test_start_app():
    from app.state import State, INIT, NORMAL
    state = State([INIT, NORMAL])
    
    assert state.is_(INIT)
    emit(event.start_app)

    assert state.is_(NORMAL)


def test_quit():
    quited = False

    class Mock:
        def handle_quit(self, a, b):
            nonlocal quited
            quited = True
    
    __.Application = Mock()

    emit(event.quit)

    assert quited

def test_styles_with_emit():
    from app.style import Style

    label = Gtk.Label(label="text")
    style_context = label.get_style_context()
    
    style = Style()
    assert style
    
    style.registry.append(join(dirname(__file__), 'styles/app.css'))
    assert len(style.registry) == 1

    emit(event.load_styles)

    # see if it's red
    color = style_context.get_color(Gtk.StateFlags.NORMAL)
    assert color.blue == 1.0 and color.red == 0.0 and color.green == 0.0

    # add test css
    style.registry.append(join(dirname(__file__), 'styles/test.css'))
    assert len(style.registry) == 2

    emit(event.reset_styles)

    # see if it's blue
    color = style_context.get_color(Gtk.StateFlags.NORMAL)
    assert color.blue == 0.0 and color.red == 1.0 and color.green == 0.0

    # reset all
    style.registry = []
    style.registry.append(join(dirname(__file__), 'styles/app.css'))
    assert len(style.registry) == 1    

    emit(event.reset_styles)

    color = style_context.get_color(Gtk.StateFlags.NORMAL)
    assert color.blue == 1.0 and color.red == 0.0 and color.green == 0.0
