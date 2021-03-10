from app.register import Register as __
from copypaster import log, PROJECT_DIR
import os
from app.signal_bus import emit, subscribe
from copypaster.file_loader import load_snippets
from copypaster.widgets.containers import ButtonGrid, ButtonTree


@subscribe
def start_app():
    load_config()
    emit('load_style', os.path.join(PROJECT_DIR, "copypaster", "app.css"))


@subscribe
def quit():
    log.debug("Quitting...")


def load_config():
    """Here we load dirty notes (first) and then the rest of the
    notes.

    On event: start_app"""
    log.debug("Loading config")

    snippets = __.Snippets

    snippets.initialize(*load_snippets())
    snippets.show_root()
    snippets.show()
    
    __.main_window.show_all()  # redraw everything


@subscribe
def change_button_grid(current_position, destination):

    log.debug(f"Switch to the other branch from {current_position} to  {destination}")
    snippets = getattr(__, "Snippets")

    snippets.goto(destination)
