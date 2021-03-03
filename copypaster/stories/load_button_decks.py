import os
import threading, queue
from app.register import Register as __
from copypaster import log, PROJECT_DIR
import os
from app.signal_bus import emit, subscribe
from copypaster.file_loader import Deck, Snippet
from copypaster.widgets.notebooks import ButtonGrid, ButtonCollection

BACKUP_FOLDER = "/home/kris/workshops/tools/copypaster/file_decks"

PATH_TO_SNIPPETS_FOLDER = os.environ.get('SNIPPETS_FOLDER', BACKUP_FOLDER)


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
    log.debug("LoadButtonDecks is run")

    cabinet = __.FileCabinet

    load_snippets(cabinet)

    __.main_window.show_all()  # redraw everything

    set_visibility_on_collections()


def load_snippets(cabinet):
    log.debug("Loading snippets")

    line = queue.Queue()

    Decks = {}
    Decks_Data = {}

    join = os.path.join

    def read(entry):

        if entry.is_file():
            snippet = Snippet().load(entry.path)
            
                        try:
                self.add_button(**_button)
            except IndexError:
                pass  # yes, cause this value exists
            except AssertionError:
                log.error("No-value entry in deck {}".format(self.path))
                exit(1)
            return ('file', f"name: {entry.name}", f"path: {entry.path}")

        if entry.is_dir():
            return NavigateButton(  # is what we will display
                    label=destination,
                    report_to=collection_name,
                    current=name,
                    target=target_name,
                )
            return ('dir', f"name: {entry.name}", f"path: {entry.path}")

    def walk(folder):
        global line
        global Decks
        global Decks_Data
        deck = ButtonGrid()

        # navigate to parent
        deck.append(NavigateButton(
            label="..", report_to=collection_name, current=name, target=folder
        ))

        # TODO: here i can read a file with metadata

        with os.scandir(folder) as it:
            for entry in it:
                if entry.name.startswith('.'):
                    continue

                if entry.is_dir():
                    line.put(entry.path)

                deck.append(read(entry))

        deck.hide()

        Decks[folder] = deck
        Decks_Data[folder] = {'name': os.path.basename(folder)}

    def worker():
        while True:
            folder = line.get()
            print(f'Working on folder: {folder}')

            walk(folder)
            print(f'Finished {folder}')
            line.task_done()

    threading.Thread(target=worker, daemon=True).start()

    line.put(PATH_TO_SNIPPETS_FOLDER)

    # block until all tasks are done
    line.join()

    """TODO : I need the decks as widgets that will
    contain the buttons.

    then add all to some other widget. 
     and hide them all.
    then show the first.

    navigate buttons will on click show deck 
    that has their path."""

    root_deck = Decks[PATH_TO_SNIPPETS_FOLDER]

    cabinet.add_page("Snippets", root_deck)

    setattr(__, 'Decks', Decks)
    setattr(__, 'Decks_Data', Decks_Data)
    setattr(__, 'Snippets', root_deck)


def set_visibility_on_collections(collections):
    """We must hide all objects on collections and show all roots"""
    for collection in collections:
        collection.hide_all_grids()
        collection.show_root()


@subscribe
def change_button_grid(report_to, current, target):

    log.debug(
        "Switch to the other branch from {} to  {} in {}".format(
            current, target, report_to
        )
    )
    collection = getattr(__, report_to)  # get the collection from register
    collection.current = target

    # The whole secret to navigation is that nothing moves.
    # All is static, we only show and hide stuff"
    collection.grids[current].hide()
    collection.grids[target].show()
