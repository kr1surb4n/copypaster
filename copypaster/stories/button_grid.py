from app.register import Register as __
from copypaster import log
import os
import copypaster.events as event
from app.signal_bus import subscribe, subscribe_on
from copypaster.file_loader import load_snippets, load_folder


@subscribe_on(event.start_app)
def initialize_snippets():
    """Here we load snippets into Snippets object

    On event: start_app"""
    log.debug("Loading snippets")

    __.Snippets.initialize(*load_snippets())
    change_button_grid("Starting", __.Snippets.root)
    __.Snippets.show()

    __.MainWindow.show_all()  # redraw everything


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
