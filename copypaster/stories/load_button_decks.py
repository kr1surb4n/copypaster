from app.register import Register as __
from copypaster import log, PROJECT_DIR
import os
from app.signal_bus import emit, subscribe
from copypaster.file_loader import load_snippets, load_folder
from copypaster.widgets.containers import ButtonGrid, ButtonTree


@subscribe
def start_app():
    initialize_snippets()
    emit('load_style', os.path.join(PROJECT_DIR, "copypaster", "app.css"))


def initialize_snippets():
    """Here we load dirty notes (first) and then the rest of the
    notes.

    On event: start_app"""
    log.debug("Loading snippets")

    __.Snippets.initialize(*load_snippets())
    change_button_grid("Starting", __.Snippets.root)
    __.Snippets.show()

    __.main_window.show_all()  # redraw everything


@subscribe
def change_button_grid(current_position, destination):
    log.debug(f"Switch to the other branch from {current_position} to  {destination}")

    destination_grid = __.Snippets.tree[destination]

    if destination_grid.is_empty:
        log.debug("Grid is empty, loading...")

        load_folder(destination_grid)

    __.Snippets.goto(destination)
    show_current_possition_as(destination)


def show_current_possition_as(destination):
    __.LevelIndicator.set_text(os.path.basename(destination))
