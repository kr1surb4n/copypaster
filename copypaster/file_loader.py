import yaml
import os
import threading, queue
from pathlib import Path
import configparser
import yaml
import string

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk  # noqa

from copypaster.widgets.buttons import Copy, GoTo
from copypaster.widgets.containers import ButtonTree, ButtonGrid
from copypaster import log, PROJECT_DIR

tasks = queue.Queue()
Decks = {}

BACKUP_FOLDER = os.path.join(PROJECT_DIR, "file_decks")
PATH_TO_SNIPPETS_FOLDER = os.environ.get('SNIPPETS_FOLDER', BACKUP_FOLDER)

CLICK_COUNT = "click_count"
INFO = "info"
NAME = "name"
VALUE = "value"
BUTTONS = "buttons"
CATEGORY = "category"
SNIPPET = "snippet"
CONTENT = "content"
INFO = "info"

MAX_FILENAME_LENGTH = 18

join = os.path.join

rules = str.maketrans('', '', string.punctuation)

name_counter = 1

def placeholder_name():
    _lock = threading.Lock()
    with _lock:
        global name_counter
        name = f"snippet_{name_counter}"
        name_counter += 1

    return name

def clean_name(name: str):

    if name is None:
        name = "None"

    name = name.strip()

    if len(name) > MAX_FILENAME_LENGTH:
        name = name[:MAX_FILENAME_LENGTH]

    return name

def clean_filename(name: str):

    if name is None:
        name = "None"


    name = name.strip()
    name = name.translate(rules)

    if len(name) > MAX_FILENAME_LENGTH:
        name = name[:MAX_FILENAME_LENGTH]

    if len(name) == 0:
        name = placeholder_name()

    return name.replace(" ", "-")

class Folder:
    def __init__(self, name="", path=""):
        self.name = name
        self.path = path

    def suffix_path(self, path_to_containing_folder):
        self.path = os.path.join(path_to_containing_folder, self.name)

    def save(self):
        os.mkdir(self.path)

    def delete(self):
        os.unlink(self.path)


class Snippet:
    def __init__(self, name="", content="", path=""):

        self.name = clean_name(name)
        self.filename = clean_filename(name)

        self.path = path
        self.content = content


    def prefix_filename_with(self, path_to_containing_folder):
        self.path = os.path.join(path_to_containing_folder, self.filename)

    # TODO: fix where the populate is
    def populate(self, snippet_dictionary: dict):
        self.content = str(snippet_dictionary.get(VALUE, ""))
        self.name = str(snippet_dictionary.get(NAME, clean_name(self.content)))
        
        return self

    def load(self, path: str):
        self.path = path

        with open(path, 'r') as f:
            content = f.readlines()

        # f"# name: {self.name}\n"
        self.name = content[0][8:].strip()
        self.content = "".join(content[1:])

        return self

    def save(self):
        with open(self.path, 'w') as f:
            f.write(f"# name: {self.name} \n")
            f.write(self.content)

        return self

    def delete(self):
        os.unlink(self.path)


def button_made_from(entry: os.DirEntry) -> Gtk.Button:

    if entry.is_file():
        return Copy(Snippet().load(entry.path))

    if entry.is_dir():
        return GoTo(
                name=entry.name,
                position=os.path.dirname(entry.path),
                destination=entry.path,
            )
        
def walk(folder: str):
    global Decks
    global Decks_Data
    global tasks

    deck = ButtonGrid()

    parent_folder = os.path.dirname(folder)

    if folder != PATH_TO_SNIPPETS_FOLDER:
        deck.add_go_to_parent_button(folder, parent_folder)

    # TODO: here i can read a file with metadata

    with os.scandir(folder) as it:
        for entry in it:
            if entry.name.startswith('.'):
                continue

            if entry.is_dir():
                tasks.put(entry.path)

            deck.append(button_made_from(entry))

    deck.show()
    Decks[folder] = deck

def worker():
    global tasks

    while True:
        folder = tasks.get()
        log.debug(f'Working on folder: {folder}')

        walk(folder)
        log.debug(f'Finished {folder}')
        tasks.task_done()


def load_snippets() -> (dict, str):
    log.info('Loading snippets')
    global tasks
    global Decks

    # turn-on the worker thread
    threading.Thread(target=worker, daemon=True).start()

    tasks.put(PATH_TO_SNIPPETS_FOLDER)

    # block until all tasks are done
    tasks.join()

    return Decks, PATH_TO_SNIPPETS_FOLDER

    log.info('All snippets loaded')
